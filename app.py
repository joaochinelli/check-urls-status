import csv, grequests

list_itens_ok = []
list_itens_error = []

def create_csv_file(dir_name_file, listItens):
  with open(dir_name_file, 'w') as csvfile:
    for item in listItens:
      writer = csv.writer(csvfile)
      writer.writerow(item)
    csvfile.close()

def file_csv(dir_file, base_url):
  rows = []
  try:
    with open(dir_file, 'r', newline='', encoding='utf-8') as file_csv:
      reader_csv = csv.reader(file_csv)
      for row in reader_csv:
        if row[0] != 'Redirect from':
          if 'http' not in row[1]:
            row[1] = f"{base_url}{row[1]}"
          rows.append(row)
        else: 
          headerFile = row

  except FileNotFoundError:
    print(f"file '{dir_file}' not found.")
  except Exception as e:
    print(f"Error: {e}")

  return rows

def divide_blocks(array, tamanho_bloco):
    return [array[i:i+tamanho_bloco] for i in range(0, len(array), tamanho_bloco)]

def check_url(listUrls):
  try:
    requests = (grequests.get(url[1]) for url in listUrls)
    response = grequests.map(requests)

    for result in enumerate(response):
      print(f"Status code: {result[1].status_code} --> {result[1].url}")
      if result[1].status_code == 200:
        list_itens_ok.append([result[1].url])
      else:
        list_itens_error.append([result[1].url])

  except Exception as e:
        print(f"Error when making the request: {e}")
    
def main(file, base_url, limit):
  data = file_csv(file, base_url)

  if len(data) > limit:
    blocos = divide_blocks(data, limit)
  else:
    blocos = [data]

  for i, bloco in enumerate(blocos):
    print(f'Block {i + 1}')
    print('\n')
    check_url(bloco)
    print('\n\n\n')

  create_csv_file(file.replace(".csv","_status_code_200"), list_itens_ok)
  create_csv_file(file.replace(".csv","_status_code_404"), list_itens_error)

  print(f"Files {file.replace(".csv","_status_code_200")}.csv and {file.replace(".csv","_status_code_404")}.csv created with success")

file = input("Enter the name of the file csv: ")
base_url = input("Enter the base url: ")
limit = input("Enter the request limit per block (ex: 200): ")

main(file, base_url, int(limit))

