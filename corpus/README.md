Esta é uma série de scripts que podem ser utilizados para a compilação e processamento de corpora. A implementação atual reflete as minhas necessidades, dentro de uma pesquisa sobre formação de palavras. Portanto, é bem provável que ela não satisfaça as suas necessidades da forma como está. No entanto, tentei deixar o código bastante extensível, para que outras funcionalidades possam ser agregadas.

## Banco de dados

Os dados são armazenados em um banco de dados SQLite, de modo que o corpus possa ser portável, caiba em um arquivo e permita consultas super rápidas, mesmo com uma grande quantidade de dados.

O formato de armazenamento é descrito em init.py, que pode ser modificado caso haja necessidade de se ter mais metadados sobre os textos analisados e sobre as estruturas linguísticas. Por exemplo, pode-se agregar anotações linguísticas, de diversos níveis, aos textos do corpus.

## Arquivos de entrada 

O script populate.py, nesta implementação, é alimentado com um arquivo JSON contendo uma lista de objetos [ {...} {...} ... ]. Cada objeto contém as seguintes chaves: 'url', 'titulo', 'corpo', 'data' e 'hash'.
