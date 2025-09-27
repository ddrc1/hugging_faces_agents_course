import json
import httpx
import pandas as pd
from graph.graph_state import GraphState
from graph.graph import compiled_graph


def main(questions: list[dict]):
    count = 0
    for question in questions:
        print("ID:", question["task_id"], "| level:", question["Level"], "| file required:", question["file_name"])
        
        response = compiled_graph.invoke(GraphState(question=question["Question"], file_name=question["file_name"]))
        print(response)
        
        print(f"Right answer: {question["Final answer"]}", "| Response:", response['answer'])
        
        if question["Final answer"].lower() == response['answer'].lower():
            count += 1
        
    print("Right answers:", count)


if __name__ == "__main__":
    file_path = "./GAIA/2023/validation/metadata.jsonl"
    questions: list[dict] = []
    with open(file_path, "r") as f:
        for line in f:
            linha_limpa = line.strip()
            if linha_limpa:
                questions.append(json.loads(linha_limpa))
    
    selected_questions = httpx.get("https://agents-course-unit4-scoring.hf.space/questions").json()
    
    questions_df = pd.DataFrame(questions)
    selected_questions_df = pd.DataFrame(selected_questions)
    
    questions_df = questions_df.merge(selected_questions_df[["task_id"]], on="task_id", how="inner")
    questions_df.reset_index(drop=True, inplace=True)
    questions = questions_df.to_dict(orient="records")
    main(questions)
    # Best: 14/20