# 🎯 Tiro e Mosca com Redes  

Um jogo multiplayer desenvolvido em Python utilizando a biblioteca Pygame! Jogue contra o computador ou desafie um amigo no modo multijogador.  

---

## 📌 Pré-requisitos  
- Python **3.10** ou superior  

## 🔧 Instalação  

Antes de começar, instale a biblioteca necessária executando:  

```sh
pip install pygame
```

---

## 🌐 Configuração de IP  

Para conectar os jogadores na mesma rede, siga os passos abaixo:  

### 1️⃣ Descubra o IP do servidor  

- **Linux**: Execute o comando abaixo e copie o endereço IP:  
  ```sh
  ifconfig
  ```  
- **Windows**: Execute no terminal:  
  ```sh
  ipconfig
  ```

### 2️⃣ Adicione o IP ao projeto  

- No arquivo **`server_tiroMosca.py`**, substitua `'ip'` pelo IP do servidor:  
  ```python
  server = 'ip'
  ```  
- No arquivo **`network.py`**, também substitua `'ip'` pelo IP do servidor:  
  ```python
  self.server = 'ip'
  ```
  
---

## ▶️ Como jogar  

### 🏹 Iniciando o servidor  
No terminal, execute:  

```sh
python server_tiroMosca.py
```
ou

```sh
python3 server_tiroMosca.py
```

### 🎮 Jogando  

#### Modo **vs Computador**  
Execute apenas um cliente:  

```sh
python client_tiroMosca.py
```  
ou
```sh
python3 client_tiroMosca.py
```  
E escolha a opção **"Computador"** no menu.  

#### Modo **Multijogador**  
Em **dois terminais diferentes**, execute:  

```sh
python client_tiroMosca.py
```  
ou
```sh
python3 client_tiroMosca.py
```  
Ambos os jogadores devem selecionar a opção **"2 jogadores"**.  

🔥 **Divirta-se!**  

---

## 👨‍💻 Autores  

Desenvolvido por:  
- **[Diego Sanches](https://github.com/iamdiegosanches)**  
- **[Álvaro Braz](https://github.com/oalvarobraz)**  

Projeto criado com ❤️ por alunos da **Universidade Federal de Ouro Preto** 🎓  
