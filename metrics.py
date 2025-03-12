from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)
from mlxtend.plotting import plot_confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
import psycopg2

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

        sql = "SELECT expected_response, ai_response FROM image_analysis WHERE model = 'google-paligemma-224' AND database = 'vote-request-v2' AND prompt_strategy = 'zero-shot-observatiom';"

        cursor.execute(sql)
        results = cursor.fetchall()

        true = [row[0].split("\n")[0] for row in results]
        prediction = [row[1].split("\n")[0] for row in results]

        # print(true)
        # print(prediction)

        cm = confusion_matrix(true, prediction, labels=["Yes", "No"])
        print(f"Matriz de confusão:\n{cm}")

        tp = cm[0, 0]  # True Positives
        fp = cm[1, 0]  # False Positives
        fn = cm[0, 1]  # False Negatives
        tn = cm[1, 1]  # True Negatives

        print(f"True Positives (TP): {tp}")
        print(f"False Positives (FP): {fp}")
        print(f"False Negatives (FN): {fn}")
        print(f"True Negatives (TN): {tn}")

        fig, ax = plot_confusion_matrix(
            conf_mat=np.array(cm), show_absolute=True, show_normed=True, colorbar=True
        )
        plt.show()

        # print(true)
        # print(prediction)
        accuracy = accuracy_score(true, prediction)
        precision = precision_score(true, prediction, pos_label="Yes")
        recall = recall_score(true, prediction, pos_label="Yes")
        f1 = f1_score(true, prediction, pos_label="Yes")

        print(f"Accuracy: {accuracy:.2f}")
        print(f"Precision: {precision:.2f}")
        print(f"Recall: {recall:.2f}")
        print(f"F1 Score: {f1:.2f}")

    except connection.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
    finally:
        if connection.isexecuting():
            cursor.close()
            connection.close()
