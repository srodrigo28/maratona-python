### pandas
import pandas as pd

# Criando um DataFrame simples
dados = {
    'Nome': ['Ana', 'Bruno', 'Carlos'],
    'Idade': [25, 30, 22]
}

df = pd.DataFrame(dados)

# Exibindo o DataFrame
print(df)
