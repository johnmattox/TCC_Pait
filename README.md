### A revolta da armada e os telegramas de Benham

Repositório para versionamento de códigos relativos  
ao TCC orientado pelo prof. Pait em 2018.

#### Alunos:
* César Augusto Mendes Tersariolli
* John Mendes Mattox

### Sobre os códigos:

Os códigos foram dividos em três pastas:
* U-NET: Encontram-se todos os códigos relativos ao pré-tratamento das imagens com a rede U-NET para a geração da base de dados;
* OCR: Encontram-se todos os códigos relativos a conversão das imagens para uma base de dados com o Tesseract;
* Decifragem: Encontram-se todos os códigos relativos decifragem das mensagens do código de Slater com a base de dados gerada com o Tesseract.;

### U-NET:

Contém multiplos arquivos que cobrem as tarefas de gerar as imagens sintéticas até aplicar a rede neural nas imagens do código. Cada arquivo será descrito abaixo:
* notebook_gerar_imagens_sintéticas: Programa para gerar as imagens sintéticas, conforme descrito no relatório final. Usa a base de dados jules_verne.txt para extrair as palavras;
* notebook_gerar_imagens_sintéticas_slaters: Programa para gerar as imagens sintéticas, com a diferença de gerar imagens sintéticas similares as páginas do código de Slater, conforme descrito no relatório final. Usa a base de dados jules_verne.txt para extrair as palavras;
* gera_cjtos: Coleta as imagens sintéticas de um diretório e gera os conjuntos de teste e de treino para a rede neural;
* train_unet: Executa o treino da rede a partir dos diretórios de conjuntos de testes e de treinos;
* train_unet_especifica: Executa o treino da rede a partir dos diretórios de conjuntos de testes e de treinos, com a diferença de trabalhar com as imagens sintéticas no formato do código de Slater;
* pred_img: Coleta os pesos da rede e aplica a U-NET a um conjunto de imagens. Os pesos podem ser os gerados pelos treinamentos dos códigos aqui descritos, ou pesos gerados por outros programas (pesos encontrados na internet, por exemplo).

Os arquivos data.py e jules_verne.txt são arquivos necessários para o funcionamento dos outros programas, então devem baixados em conjunto.

### OCR:

Contem um único arquivo "Gera Base de Dados" que pega as imagens de um diretório e aplica o algoritmo descrito no relatório final para gerar a base de dados. A ideia do Algoritmo é, através da biblioteca pytesseract, extrair os textos das imagens, trata-los e preencher a base de dados.

### Decifragem:

Contem um único arquivo "Decifragem" que pega a base de dados e as mensagens de um diretório e aplica o algoritmo descrito no relatório final para decifrar as mensagens. A ideia do Algoritmo é cruzar os dados das mensagens com a base de dados e a partir dai, decifrar as mensagens.
