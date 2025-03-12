import requests
import json
import subprocess
import mimetypes
import base64
import os
import random
import shutil
import psycopg2
import time

endpoint = "u"
region = ""
project_id = ""
url = f"https://{endpoint}/v1beta1/projects/{project_id}/locations/{region}/endpoints/openapi/chat/completions"


def get_aleatory_file(dir_path):
    try:
        files_list = [
            os.path.join(dir_path, arquivo) for arquivo in os.listdir(dir_path)
        ]
        if files_list:
            aleatory_file = random.choice(files_list)
            return {
                "file_path": aleatory_file,
                "file_id": os.path.basename(aleatory_file),
            }
        else:
            print(f"A pasta '{dir_path}' está vazia.")
            return None
    except FileNotFoundError:
        print(f"Erro: A pasta '{dir_path}' não foi encontrada.")
        return None


def move_file(fil_path, destination_path="./already-sended"):
    if not os.path.exists(destination_path):
        try:
            os.mkdir(destination_path)
            print(f"Pasta '{destination_path}' criada com sucesso!")
        except OSError as e:
            print(f"Erro ao criar a pasta '{destination_path}': {e}")
    shutil.move(fil_path, destination_path)


def encode_image_to_data_uri(image_path):
    mime_type, _ = mimetypes.guess_type(image_path)
    if mime_type is None:
        raise ValueError("Não foi possível determinar o MIME type do arquivo.")

    with open(image_path, "rb") as image_file:
        encoded_bytes = base64.b64encode(image_file.read())
        encoded_string = encoded_bytes.decode("utf-8")

    return f"data:{mime_type};base64,{encoded_string}"


def get_access_token():
    try:
        # Isso aqui não funciona, estava gerando os token manualmente no terminal quando o token antigo ficava inválido
        # Executa o comando e captura a saída
        result = subprocess.run(
            ["gcloud", "auth", "print-access-token"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("Erro ao executar o comando:", e.stderr)
        return None


def make_request(image_data_uri, prompt, cursor, connection, image_id):
    # Conteúdo da requisição
    request_data = {
        "model": "meta/llama-3.2-90b-vision-instruct-maas",
        "stream": False,
        "temperature": 0.5,
        "top_p": 0.95,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": image_data_uri},
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_access_token()}",
    }

    response = requests.post(url, headers=headers, json=request_data)

    if response.status_code == 200:
        ai_response = response.json()["choices"][0]["message"]["content"]

        sql = "INSERT INTO image_analysis (image_id, database, prompt_strategy, prompt, model, expected_response, ai_response) VALUES (%s, %s, %s, %s, %s, %s, %s)"

        expected_response = "Yes" if "S" in image_id else "No"

        val = (
            image_id,
            "vote-request--v2",
            "zero-shot-observation",
            prompt,
            "llama-3.2-90b-vision",
            expected_response,
            ai_response,
        )

        cursor.execute(sql, val)
        connection.commit()
        print(f"Análise da imagem {image_id} concluída com sucesso!")

    else:
        print("Erro:", response.status_code, response.text)
        print("Trocar token, 1000 segundos restantes")
        time.sleep(1000)


if __name__ == "__main__":
    try:
        connection = psycopg2.connect(
            database="db_name",
            user="user",
            host="host",
            password="password",
            port=5432,
        )
        cursor = connection.cursor()

        prompt = ""

        with open("./zero-shot-obs-vote-request.txt", "r") as file:
            prompt = file.read()
            file.close()

        # Fazer o Loop Aqui
        while True:
            aleatory_file = get_aleatory_file("C:/Users/Admin/Downloads/Pedido de voto")
            if aleatory_file:
                # image_path = f"https://storage.googleapis.com/teste-imagens-pli/{aleatory_file["file_id"]}"
                # print(image_path)
                image_path = encode_image_to_data_uri(aleatory_file["file_path"])
                make_request(
                    image_data_uri=image_path,
                    prompt=prompt,
                    cursor=cursor,
                    connection=connection,
                    image_id=aleatory_file["file_id"].split(".")[0],
                )
                move_file(aleatory_file["file_path"], "./already-sended")
                time.sleep(15)
            else:
                break

    except connection.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
    finally:
        if connection.isexecuting():
            cursor.close()
            connection.close()
