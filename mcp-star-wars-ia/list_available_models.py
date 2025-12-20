import google.generativeai as genai
import os
from dotenv import load_dotenv

# Carrega a chave de API do arquivo .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Erro: A chave da API do Gemini não foi encontrada no arquivo .env.")
else:
    genai.configure(api_key=api_key)
    print("Buscando modelos disponíveis para sua chave de API...\n")
    
    try:
        model_list = genai.list_models()
        
        print("Modelos que suportam 'generateContent' (necessário para o nosso app):")
        found_model = False
        for m in model_list:
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
                found_model = True

        if not found_model:
            print("\nNenhum modelo com suporte a 'generateContent' foi encontrado.")
            print("Lista completa de modelos retornados pela API:")
            for m in model_list:
                 print(f"- {m.name} (Suporta: {m.supported_generation_methods})")

    except Exception as e:
        print(f"\nOcorreu um erro ao tentar listar os modelos: {e}")
        print("Por favor, verifique se sua chave de API é válida e tem as permissões necessárias.")
