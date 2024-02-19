"""Taller evaluable"""

import glob

import pandas as pd

# pip3 install pyarrow pandas
# python -m venv .venv
# .venv\Scripts\activate
# pip3 install --update pip

# Primera salida: ['input\\file1.txt', 'input\\file2.txt', 'input\\file3.txt', 'input\\file4.txt']

def load_input(input_directory):
    """Load text files in 'input_directory/'"""
    #
    # Lea los archivos de texto en la carpeta input/ y almacene el contenido en
    # un DataFrame de Pandas. Cada línea del archivo de texto debe ser una
    # entrada en el DataFrame.
    #
    filenames = glob.glob(input_directory + "/*.*")
    dataframes = [
        pd.read_csv(filename, sep=";", names=['text']) for filename in filenames
    ]
    dataframe = pd.concat(dataframes).reset_index(drop=True)
    
    return dataframe

#.str.replace(r'[^\w\s]', '')

def clean_text(dataframe):
    """Text cleaning"""
    #
    # Elimine la puntuación y convierta el texto a minúsculas.
    #
    dataframe = dataframe.copy()
    dataframe['text'] = dataframe['text'].str.lower()
    dataframe['text'] = dataframe['text'].str.replace(',', '').str.replace('.', '')
    
    return dataframe

# dataframe = dataframe.groupby('text').size().reset_index(name='count')
# dataframe = dataframe.sort_values('count', ascending=False)

def count_words(dataframe):
    """Word count"""
    dataframe = dataframe.copy()
    dataframe['text'] = dataframe['text'].str.split()
    dataframe = dataframe.explode('text').reset_index(drop=True)  # para que cada palabra sea una fila separada
    dataframe = dataframe.rename(columns={'text': 'word'})
    dataframe['count'] = 1
    conteo = dataframe.groupby('word', as_index=False).agg(
        {
            'count': sum
        }
    )
    
    return conteo


def save_output(dataframe, output_filename):
    """Save output to a file."""
    dataframe.to_csv(output_filename, index=False, sep=";")


#
# Escriba la función job, la cual orquesta las funciones anteriores.
#
def run(input_directory, output_filename):
    """Call all functions."""
    dataframe = load_input(input_directory)
    dataframe = clean_text(dataframe)
    dataframe = count_words(dataframe)
    save_output(dataframe, output_filename)


if __name__ == "__main__":
    run(
        "input",
        "output.txt",
    )
