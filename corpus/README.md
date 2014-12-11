Este é um conjunto de scripts que podem ser usados para a compilação e processamento de corpora. A implementação atual reflete as minhas necessidade dentro de uma projeto sobre formação de palavras. Portanto, é bem provável que ela não satisfaça as suas necessidades da forma como está. No entanto, tentei deixar o código bastante extensível, para que outras funcionalidades possam ser agregadas a ele.

## Banco de dados

Os dados são armazenados em um banco de dados SQLite, de modo que os corpora sejam bastante portáveis, caibam em um arquivo apenas e permitam consultas super rápidas, mesmo com uma grande quantidade de dados.

O formato de armazenamento é descrito em init.py, que pode ser modificado caso haja necessidade de se ter mais metadados sobre os textos analisados e sobre as estruturas linguísticas. É possível, por exemplo, adicionar anotações linguísticas, de diversos níveis, aos textos do banco de dados.

## Arquivos de entrada 

O script populate.py, nesta implementação, é alimentado com um arquivo JSON contendo uma lista de objetos [ {...} {...} ... ]. Cada objeto contém as seguintes chaves: 'url', 'titulo', 'corpo', 'data' e 'hash'.

## Mais...

Esse README pode não ser suficiente para você, e o código não está suficientemente documentado. Entre em contato, pergunte e tenha paciência...
