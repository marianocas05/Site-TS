# Desenvolvimento da aplicação da 2ª parte do projeto


## Programação

A estrutura deverá ser similar à da aplicação MovieStreamApp que se viu nas aula ([código no GitHub](https://github.com/edrdo/MovieStreamApp)):


### Exemplo na MovieStreamApp 

(entre vários outros) 

Informação de um filme - "endpoint" `/movies/int:id`:

- [Código no método `get_movie` em app.py](https://github.com/edrdo/MovieStreamApp/blob/master/app.py#L46)
- [Template em `templates/movie.html`](https://github.com/edrdo/MovieStreamApp/blob/master/templates/movie.html)

### Sumário das principais tags usadas no código da MovieStreamApp

#### Jinja

- `{{ x.attr }}` : expande para valor de atributo  `attr` para variável `x` -  [[ver documentação]](https://jinja.palletsprojects.com/en/3.0.x/templates/#variables) 
- `{% for x in items %} ... {% endfor %}`: iteração `for`sobre lista de valores `items` [[ver documentação]](https://jinja.palletsprojects.com/en/3.0.x/templates/#for)


#### HTML (com apontadores para tutorial W3 Schools)

- `<a href ...>`: [links](https://www.w3schools.com/html/html_links.asp)
- `<table> <th> <tr> <td>`: [formatação de tabelas](https://www.w3schools.com/html/html_tables.asp)
- `<ul>`, `<ol>` `<li>`: [formatação de listas](https://www.w3schools.com/html/html_lists.asp)
- `<h1>, <h2>, ...`: [cabeçalhos de nível 1, 2, ...](https://www.w3schools.com/html/html_headings.asp)
- `<p>`: [parágrafos](https://www.w3schools.com/html/html_paragraphs.asp)
- `<b>, <i>, ...`: [formatação de texto em negrito, itálico, ...](https://www.w3schools.com/html/html_formatting.asp)


## Instalação de software

Precisas de ter o Python 3 e o gestor de pacotes pip instalado.


```
sudo apt-get install python3 python3-pip
```

Tendo Python 3 e pip instalados, deves instalar a biblioteca `Flask` executando o comando:

```
pip3 install --user Flask
``` 

## Mais referências

- [Aplicações BD com SQL embebido](https://moodle2324.up.pt/mod/resource/view.php?id=96059) (slides das aulas teóricas)
- [MovieStream - aplicação exemplo](https://moodle.up.pt/mod/resource/view.php?id=77946)
- HTML: 
   - [W3 schools tutorial simples](https://www.w3schools.com/html/default.asp)
   - [referência Mozilla](https://developer.mozilla.org/en-US/docs/Web/HTML) 
- Bibliotecas:
  - [sqlite3](https://docs.python.org/3/library/sqlite3.html)
  - [Flask](https://flask.palletsprojects.com/en/1.1.x/)
  - [Jinja templates](https://jinja.palletsprojects.com/en/2.10.x/templates/)
