from pytrends.request import TrendReq
import pandas as pd
import time

# Inicializa a requisição do pytrends
pytrends = TrendReq(hl='pt-BR', tz=180)

# Define a palavra-chave e constrói o payload
keywords = []

#Define quantas palavras será a consulta
n = int(input("Quantas palavras deseja pesquisar? "))
for i in range(0, n):
    keywords.append(input("Insira a palavra: "))

def fetch_data_with_retry(pytrends, keywords, retries=5, delay=60):
    for attempt in range(retries):
        try:
            pytrends.build_payload(keywords, cat=0, timeframe='today 5-y', geo='BR', gprop='')
            data = pytrends.interest_over_time()
            
            if not data.empty:
                if 'isPartial' in data.columns:
                    data = data.drop(columns=['isPartial'])
                
                filename = '_'.join(keywords) + '_trends.csv'
                data.to_csv(filename)
                print(f"Dados para {', '.join(keywords)} foram exportados para {filename}")
                return data
            else:
                print(f"Nenhum dado encontrado para {', '.join(keywords)}")
                return None
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            if attempt < retries - 1:
                print(f"Tentando novamente em {delay} segundos...")
                time.sleep(delay)
            else:
                print("Número máximo de tentativas atingido.")
                return None

# Tenta obter os dados com retry
fetch_data_with_retry(pytrends, keywords)