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



### OCR:

Contem um único arquivo "Gera Base de Dados" que pega as imagens de um diretório e aplica o algoritmo descrito no relatório final para gerar a base de dados. A ideia do Algoritmo é, através da biblioteca pytesseract, extrair os textos das imagens, trata-los e preencher a base de dados.

### Decifragem:

Contem um único arquivo "Decifragem" que pega a base de dados e as mensagens de um diretório e aplica o algoritmo descrito no relatório final para decifrar as mensagens. A ideia do Algoritmo é cruzar os dados das mensagens com a base de dados e a partir dai, decifrar as mensagens.
