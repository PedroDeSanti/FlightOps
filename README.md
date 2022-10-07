<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-3-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

# FlightOps

Ferramenta Ligeiramente Inteligente para Gestão de Horários e Trajetos Operacionais e Prestação de Serviços 

# Requisitos do Projeto:
Para realizar a instalação do projetos, pressupõe-se que seu computador já apresente Python (versão mínima 3.x) instalado. Visite [este link](https://www.python.org/downloads/) para mais informações

# Instalação do Projeto:

## Etapa 1: Instalação do Projeto
Para instalar o projeto FlightOps, será realizada a clonagem do repositório. Utilizando seu Terminal de Comando preferido, navegue até a pasta destinada ao projeto, como por exemplo:
```bash
cd C:\Users\Usuario\Desktop\MelhorProjetoDeLabSoft
```
Para clonar utilizando o protocolo HTTPS, utilize o comando abaixo:
```bash
git clone https://github.com/PedroDeSanti/FlightOps.git
```
Para clonar utilizando o protocolo SSH, utilize o comando abaixo:
```bash
git clone git@github.com:PedroDeSanti/FlightOps.git
```

## Etapa 2: Criação do ambiente virtual
Inicialmente é necessário criar o ambiente virtual para executar o projeto, para isso abra o Powershell e execute o seguinte comando:

```bash
python -m venv FlightOps
```

Em sequência, ative esse ambiente virtual usando:
```bash
.\FlightOps\bin\Activate.ps1
```

## Etapa 3: Instalação do Django
Como o projeto foi desenvolvido em Django, para utilizá-lo é necessário ter a biblioteca instalada em sua máquina. Caso ela já esteja instalada, por favor avance para a etapa seguinte.

Rode, em seu terminal de comando favorito, o seguinte comando, que realiza o download e instalação da biblioteca Django:
```bash
pip install django
```

## Etapa 4:  Executando o Projeto Localmente
Estando, pelo seu Terminal de Comando preferido, na pasta do projeto, navegue até a pasta FlightOps por meio do comando abaixo:
```bash
cd FlightOps
```
e em seguida rode o comando
```bash
python manage.py runserver
```

Com isso, ao acessar o link http://localhost:8000/FIRST/, você deverá visualizar o texto "PCS3642 - Laboratório de Engenharia de Software I, também conhecida como a MELHOR matéria da USP 🥇".

*PARABÉNS, VOCÊ CONSEGUIU RODAR O PROJETO 🎉🎉🎉*

# Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center"><a href="https://github.com/GabZamba"><img src="https://avatars.githubusercontent.com/u/98465378?v=4?s=100" width="100px;" alt="Gabriel Zambelli"/><br /><sub><b>Gabriel Zambelli</b></sub></a><br /><a href="https://github.com/PedroDeSanti/FlightOps/commits?author=GabZamba" title="Code">💻</a> <a href="https://github.com/PedroDeSanti/FlightOps/commits?author=GabZamba" title="Documentation">📖</a></td>
      <td align="center"><a href="https://github.com/jvtdegelo"><img src="https://avatars.githubusercontent.com/u/64590453?v=4?s=100" width="100px;" alt="jvtdegelo"/><br /><sub><b>jvtdegelo</b></sub></a><br /><a href="https://github.com/PedroDeSanti/FlightOps/commits?author=jvtdegelo" title="Code">💻</a> <a href="https://github.com/PedroDeSanti/FlightOps/commits?author=jvtdegelo" title="Documentation">📖</a></td>
      <td align="center"><a href="https://github.com/PedroDeSanti"><img src="https://avatars.githubusercontent.com/u/62271285?v=4?s=100" width="100px;" alt="Pedro de Santi"/><br /><sub><b>Pedro de Santi</b></sub></a><br /><a href="https://github.com/PedroDeSanti/FlightOps/commits?author=PedroDeSanti" title="Code">💻</a> <a href="https://github.com/PedroDeSanti/FlightOps/commits?author=PedroDeSanti" title="Documentation">📖</a></td>
    </tr>
  </tbody>
  <tfoot>
    
  </tfoot>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

