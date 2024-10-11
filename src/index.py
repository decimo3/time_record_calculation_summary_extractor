#!/usr/bin/python
# coding: utf8
#region imports
import os
import sys
import re
import pandas
from pypdf import PdfReader
from Scheme import Registry
#endregion imports

def get_decimal_time_from_time_string(time: str) -> str:
  """ Function that transforms time of day string on decimal time """
  h, m = [int(x) for x in time.split(':')]
  return f"{h},{str(m/60).split('.')[1]}"

if __name__ == "__main__":
  if(len(sys.argv) != 2):
    raise ValueError()
  if not (os.path.exists(sys.argv[1])):
    raise FileNotFoundError()
  with open(sys.argv[1], 'rb') as file:
    reader = PdfReader(file)
    estabelecimento_texto = ''
    departamento_texto = ''
    nome_colaborador = ''
    matricula = ''
    for page_number in range(len(reader.pages)):
      page = reader.pages[page_number]
      text = page.extract_text()
      lines = text.splitlines()
      for line_number in range(len(lines)):
        line_text = lines[line_number]
        line_words = line_text.split(' ')
        # DONE - Coletar 'estabelecimento' e 'departamento'
        if(line_words[0] == 'Estabelecimento'):
          departamento_index = line_words.index('Departamento')
          estabelecimento_texto = str.join(' ', line_words[2 : departamento_index])
          departamento_texto = str.join(' ', line_words[departamento_index + 2 : len(line_words)])
          continue
        # DONE - Coletar 'matricula' e 'nome_colaborador'
        match = re.findall('^[0-9]{6}', line_words[0])
        if(len(match) == 1):
          matricula = match[0]
          nome_colaborador = str.join(' ', line_words[2:])
          continue
        # DONE - Coletar a lista de horarios
        match = re.findall('-?[0-9]{2}:[0-9]{2}', line_text)
        if(len(match) != 13): continue
        Registry['saldo_anterior'].append(get_decimal_time_from_time_string(match[0]))
        Registry['horas_negativas_quantidade'].append(get_decimal_time_from_time_string(match[1]))
        Registry['horas_negativas_compensadas_neste_periodo'].append(get_decimal_time_from_time_string(match[2]))
        Registry['horas_negativas_compensadas_outros_periodos'].append(get_decimal_time_from_time_string(match[3]))
        Registry['horas_negativas_descontadas'].append(get_decimal_time_from_time_string(match[4]))
        Registry['horas_negativas_saldo'].append(get_decimal_time_from_time_string(match[5]))
        Registry['horas_positivas_quantidade'].append(get_decimal_time_from_time_string(match[6]))
        Registry['horas_positivas_compensadas_neste_periodo'].append(get_decimal_time_from_time_string(match[7]))
        Registry['horas_positivas_compensadas_outros_periodos'].append(get_decimal_time_from_time_string(match[8]))
        Registry['horas_positivas_descontadas'].append(get_decimal_time_from_time_string(match[9]))
        Registry['horas_positivas_saldo'].append(get_decimal_time_from_time_string(match[10]))
        Registry['saldo_periodo'].append(get_decimal_time_from_time_string(match[11]))
        Registry['saldo_final'].append(get_decimal_time_from_time_string(match[12]))
        # DONE - Coletar 'periodo_inicio' e 'final_periodo'
        match = re.findall('[0-9]{2}/[0-9]{2}', line_text)
        if(len(match) == 2):
          Registry['inicio_periodo'].append(match[0])
          Registry['final_periodo'].append(match[1])
        # DONE - Define 'estabelecimento' e 'departamento' 
        Registry['estabelecimento'].append(estabelecimento_texto)
        Registry['departamento'].append(departamento_texto)
        Registry['nome_colaborador'].append(nome_colaborador)
        Registry['matricula'].append(matricula)
    dataframe = pandas.DataFrame(Registry)
    dataframe.to_csv(path_or_buf='out.csv',index=False,sep=';')
