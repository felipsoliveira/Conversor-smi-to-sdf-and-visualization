# Visualizador de Moléculas SMILES

Um visualizador e conversor de moléculas baseado em strings SMILES usando RDKit e NGLView.

## Descrição

Esta ferramenta permite a visualização de moléculas a partir de notação SMILES (Simplified Molecular Input Line Entry System) em formatos 2D e 3D. Também oferece funcionalidades para converter arquivos SMILES (.smi) para o formato Structure-Data File (.sdf).

O programa é ideal para químicos, estudantes e pesquisadores que trabalham com estruturas moleculares e precisam de uma maneira rápida de visualizar ou converter dados moleculares.

## Funcionalidades

- **Visualização de moléculas individuais**: Insira uma string SMILES e visualize a molécula em 2D e 3D
- **Visualização de arquivos SMILES**: Carregue um arquivo .smi e visualize todas as moléculas em uma grade
- **Seleção de moléculas específicas**: Escolha qual molécula visualizar de um arquivo SMILES
- **Conversão de formatos**: Converta arquivos .smi para o formato .sdf
- **Validação de SMILES**: Verifica se as strings SMILES são válidas antes de processá-las
- **Exportação para SDF**: Salve moléculas individuais ou arquivos inteiros no formato SDF

## Requisitos

- Python 3.6+
- RDKit
- NGLView
- IPython/Jupyter

## Instalação

```bash
# Instale as dependências
pip install rdkit-pypi nglview ipython
```

## Uso

### Como módulo Python

```python
# Importe o módulo
from visualizador_moleculas import visualizar_smiles, visu, d2, converter_smi_para_sdf

# Visualize uma molécula por SMILES
visualizar_smiles("CCO", "Etanol")

# Atalho para visualizar molécula por SMILES ou arquivo
visu("CCO")  # Visualiza diretamente por SMILES
visu("moleculas.smi")  # Permite escolher uma molécula do arquivo

# Visualize todas as moléculas de um arquivo em uma grade
d2("moleculas.smi")

# Converta um arquivo SMILES para SDF
converter_smi_para_sdf("moleculas.smi", "moleculas.sdf")
```

### Como programa independente

Execute o script e escolha uma das opções do menu:

```bash
python visualizador_moleculas.py
```

## Menu Principal

1. **Visualizar molécula por SMILES**: Insira uma string SMILES diretamente
2. **Ler arquivo de SMILES**: Lista as moléculas de um arquivo .smi
3. **Converter arquivo .smi para .sdf**: Converte um arquivo SMILES para o formato SDF
4. **Visualizar todas as moléculas do arquivo SMILES**: Mostra uma grade com todas as moléculas
5. **Escolher molécula específica do arquivo**: Selecione qual molécula visualizar
6. **Sair**: Encerra o programa

## Formato do Arquivo SMILES

Os arquivos SMILES (.smi) devem seguir o formato:
```
<SMILES> <Nome da molécula>
```

Exemplo:
```
CCO Etanol
CC(=O)O Ácido acético
C1=CC=CC=C1 Benzeno
```

## Exemplos

### Visualização de uma molécula simples

```python
visu("CCO")  # Visualiza o etanol
```

### Visualização de todas as moléculas em um arquivo

```python
d2("compostos.smi")  # Mostra todas as moléculas do arquivo em uma grade
```

### Escolha de uma molécula específica do arquivo

```python
visu("compostos.smi")  # Permite escolher qual molécula visualizar
```

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias.

## Licença

[MIT License]

## Contato

Para dúvidas ou sugestões, abra uma issue no repositório.
