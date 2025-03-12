import vertexai
import psycopg2
import random
import shutil
import os
import time
from vertexai.preview.generative_models import (
    GenerativeModel,
    Image,
    GenerationResponse,
)
import google.cloud.aiplatform as aiplatform


def get_aleatory_file(dir_path):
    try:
        files_list = [
            os.path.join(dir_path, arquivo) for arquivo in os.listdir(dir_path)
        ]
        if files_list:
            aleatory_file = random.choice(files_list)
            return {
                "file_path": aleatory_file,
                "file_id": os.path.basename(aleatory_file).split(".")[0],
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


def analyze_image(
    image_path: str,
    image_id: str,
    prompt: str,
    project_id: str = "",
    location: str = "",
    model: str = "google-paligemma-224",
    connection=None,
    cursor=None,
):
    try:
        vertexai.init(project=project_id, location=location)
        image = Image.load_from_file(image_path)
        gen_model = GenerativeModel(model)

        response: GenerationResponse = gen_model.generate_content([prompt, image])
        ai_response = response.text

        sql = "INSERT INTO image_analysis (image_id, database, prompt_strategy, prompt, model, expected_response, ai_response) VALUES (%s, %s, %s, %s, %s, %s, %s)"

        expected_response = "Yes" if "S" in image_id else "No"

        val = (
            image_id,
            "vote-request-v2",
            "zero-shot-observatiom",
            prompt,
            "google-paligemma-224",
            expected_response,
            ai_response,
        )

        cursor.execute(sql, val)
        connection.commit()

    finally:
        print(f"Análise da imagem {image_id} concluída com sucesso!")


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
            aleatory_file = get_aleatory_file("path_to_images")
            if aleatory_file:
                analyze_image(
                    image_path=aleatory_file["file_path"],
                    image_id=aleatory_file["file_id"],
                    prompt=prompt,
                    connection=connection,
                    cursor=cursor,
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
