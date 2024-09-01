#!/usr/bin/python
# coding: utf8
#region imports
import re
import pandas
from pypdf import PdfReader
from Scheme import Registry
#endregion imports
if __name__ == "__main__":
  with open('src\Resumo de Apurações de Ponto Mesquita.PDF', 'rb') as file:
    reader = PdfReader(file)
    estabelecimento_texto = ''
    departamento_texto = ''
    for page_number in range(len(reader.pages)):
      page = reader.pages[page_number]
      text = page.extract_text()
      lines = text.splitlines()
      for line_number in range(len(lines)):
        line_text = lines[line_number]
        line_words = line_text.split(' ')
        # TODO - Coletar 'estabelecimento' e 'departamento'
        if(line_words[0] == 'Estabelecimento'):
          departamento_index = line_words.index('Departamento')
          estabelecimento_texto = str.join(' ', line_words[2 : departamento_index])
          departamento_texto = str.join(' ', line_words[departamento_index + 2 : len(line_words)])
          continue
        # TODO - Coletar 'matricula' e 'nome_colaborador'
        match = re.findall('^[0-9]{6}', line_words[0])
        if(len(match) == 1):
          Registry['matricula'].append(match[0])
          nome_colaborador = str.join(' ', line_words[2:])
          Registry['nome_colaborador'].append(nome_colaborador)
          continue
        # TODO - Coletar a lista de horarios
        match = re.findall('-?[0-9]{2}:[0-9]{2}', line_text)
        if(len(match) != 13): continue
        Registry['saldo_anterior'].append(match[0])
        Registry['horas_negativas_quantidade'].append(match[1])
        Registry['horas_negativas_compensadas_neste_periodo'].append(match[2])
        Registry['horas_negativas_compensadas_outros_periodos'].append(match[3])
        Registry['horas_negativas_descontadas'].append(match[4])
        Registry['horas_negativas_saldo'].append(match[5])
        Registry['horas_positivas_quantidade'].append(match[6])
        Registry['horas_positivas_compensadas_neste_periodo'].append(match[7])
        Registry['horas_positivas_compensadas_outros_periodos'].append(match[8])
        Registry['horas_positivas_descontadas'].append(match[9])
        Registry['horas_positivas_saldo'].append(match[10])
        Registry['saldo_periodo'].append(match[11])
        Registry['saldo_final'].append(match[12])
        # TODO - Coletar 'periodo_inicio' e 'final_periodo'
        match = re.findall('[0-9]{2}/[0-9]{2}', line_text)
        if(len(match) == 2):
          Registry['inicio_periodo'].append(match[0])
          Registry['final_periodo'].append(match[1])
        # TODO - Define 'estabelecimento' e 'departamento' 
        Registry['estabelecimento'].append(estabelecimento_texto)
        Registry['departamento'].append(departamento_texto)
    dataframe = pandas.DataFrame(Registry)
    dataframe.to_csv(path_or_buf='out.csv',index=False,sep=';')
