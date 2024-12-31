# RotA.I - Projeto de Geração de Rotas Turísticas Inteligentes

link de acesso: https://bit.ly/rotAI

Descrição do Projeto
O RotA.I é uma aplicação web projetada para auxiliar usuários a criarem rotas turísticas personalizadas e interativas, com base em seus pontos de partida e destinos principais. A aplicação oferece uma experiência imersiva que combina a simplicidade de uso com a inteligência de APIs modernas, permitindo que os usuários explorem pontos turísticos relevantes no caminho para seus destinos.

A aplicação utiliza a Google Maps API para fornecer direções, waypoints, e localizar atrações turísticas ao longo da rota. Além disso, o sistema conta com funcionalidades de autenticação e gerenciamento de contas para que os usuários possam criar, visualizar, e gerenciar suas próprias rotas.

Funcionalidades Implementadas
Cadastro e Login de Usuários

Sistema de autenticação seguro com hashing de senhas.
Funcionalidade de login e logout para gerenciamento de sessões.
Geração de Rotas Personalizadas

Usuários podem inserir o ponto de partida e destino.
Utilização da Google Directions API para obter a rota principal.
Integração com a Google Places API para identificar pontos turísticos ao longo do caminho.
Visualização de Rotas

Exibição das rotas geradas em um mapa interativo utilizando o Leaflet.js.
Marcadores para pontos turísticos e desenho das rotas no mapa.
Trending na Sua Área

Listagem de rotas populares criadas por outros usuários, limitada a três rotas para melhor experiência de navegação.
Gerenciamento de Rotas

Cada usuário pode criar e visualizar suas rotas personalizadas.
Interface Interativa

Carrossel para destacar imagens e informações.
Design responsivo para uma experiência fluida em diferentes dispositivos.
Aprendizados do Projeto
O desenvolvimento do RotA.I proporcionou uma série de aprendizados valiosos, abrangendo diferentes aspectos de desenvolvimento web, integração de APIs e design de software. Aqui estão os principais pontos:

Backend com Flask

Configuração e estruturação de um aplicativo Flask com múltiplas rotas e templates.
Utilização de Flask-SQLAlchemy para modelagem de banco de dados.
Migração de banco de dados com Flask-Migrate.
Gerenciamento de Dados

Estruturação de modelos relacionais para usuários, rotas e pontos turísticos.
Persistência de dados no banco de dados e manipulação eficiente com SQLAlchemy.
Tratamento de dados JSON para integração com APIs externas.
Integração com APIs Externas

Configuração e uso das Google Maps API, incluindo:
Directions API: Para obter rotas entre dois locais.
Places API: Para localizar pontos turísticos no caminho.
Interpretação de dados complexos retornados por APIs (JSON parsing).
Frontend Interativo

Implementação de mapas interativos com Leaflet.js.
Construção de uma interface amigável utilizando Bootstrap.
Uso de templates Jinja2 para renderizar dados dinâmicos no frontend.
Segurança e Autenticação

Criptografia de senhas com Werkzeug.
Implementação de sessões para controle de autenticação.
Tratamento de Erros

Identificação e tratamento de exceções para uma experiência de usuário robusta.
Logs e prints para depuração durante o desenvolvimento.
Boas Práticas de Desenvolvimento

Organização modular do código.
Uso de variáveis de ambiente e configurações centralizadas para chaves de API e configurações sensíveis.
Como o Projeto Foi Estruturado
Arquivos e Pastas

app.py: Arquivo principal contendo a lógica backend.
models.py: Modelos de dados estruturados com SQLAlchemy.
config.py: Configurações do projeto, incluindo chaves e variáveis de ambiente.
templates/: Contém os arquivos HTML para renderização no frontend.
static/: Contém arquivos CSS, JavaScript e imagens.
Fluxo Principal

O usuário faz login ou cria uma conta.
Após o login, acessa a tela principal, onde pode gerar uma nova rota ou visualizar rotas populares.
Na geração de rotas, o sistema utiliza APIs externas para criar e salvar a rota no banco de dados.
O usuário pode visualizar a rota gerada em um mapa interativo.
