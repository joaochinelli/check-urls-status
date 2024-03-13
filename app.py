import csv, requests, time, os

def add_item_in_new_file(dir_name_file, item, headerFile):
  # Verifica se o arquivo existe
  if os.path.isfile(dir_name_file):
    param = 'a'
  else:
    param = 'w'

  with open(dir_name_file, param, newline='') as csvfile:
    writer = csv.writer(csvfile)
    if param == 'w':
      writer.writerow(headerFile)
    writer.writerow(item)
    csvfile.close()

def file_csv(dir_file, base_url, separator):
  rows = []
  try:
    with open(dir_file, 'r', newline='', encoding='utf-8') as file_csv:
      reader_csv = csv.reader(file_csv, delimiter=separator)
      for index, row in enumerate(reader_csv):
        #a primeira linha do arquivo é o cabeçalho
        if index > 0:
          if 'http' not in row[1]:
            row[1] = f"{base_url}{row[1]}"
          rows.append(row)
        else: 
          headerFile = row

  except FileNotFoundError:
    print(f"file '{dir_file}' not found.")
  except Exception as e:
    print(f"Error: {e}")

  return [rows, headerFile]

def check_url(listUrls, file_200, file_404):
  for index, item in enumerate(listUrls[0]):
    try:
      # Tentativa de fazer uma solicitação GET
      headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
      response = requests.get(item[1], headers=headers)

      # Verificar se a solicitação foi bem-sucedida (código de status 200)
      status_code = response.status_code

      # Se a solicitação foi bem-sucedida, imprima o conteúdo da resposta
      print('Solicitação bem-sucedida!')
      print(f"Item [{index + 1}] - Status code: {status_code} --> {item[1]}")
      if status_code == 200:
        add_item_in_new_file(file_200, item, listUrls[1])
      else:
        add_item_in_new_file(file_404, item, listUrls[1])
    
    except requests.exceptions.HTTPError as http_err:
      print(f'Erro HTTP: {http_err}')
    except requests.exceptions.RequestException as req_err:
      print(f'Erro na solicitação: {req_err}')
    except Exception as e:
      print(f'Erro inesperado: {e}')
    
    print('-----------------------------------------------------------\n\n')
    time.sleep(0.5)
    
def main(file, base_url, separator):
  data = file_csv(file, base_url, separator)

  file_200 = file.replace(".csv","_status_code_200.csv")
  file_404 = file.replace(".csv","_status_code_404.csv")

  check_url(data, file_200, file_404)

  print(f"Files {file.replace(".csv","_status_code_200")}.csv and {file.replace(".csv","_status_code_404")}.csv created with success")

file = input("Enter the name of the file csv: ")
base_url = input("Enter the base url: ")
separator = input("Enter with the separator: ")
main(file, base_url, separator)