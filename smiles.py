import os
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Draw
from rdkit.Chem import rdmolfiles
import nglview as nv
from IPython.display import display

def ler_arquivo_smiles(caminho_arquivo):
    print(f"Tentando ler arquivo: {caminho_arquivo}")

    # Verifica se o caminho do arquivo existe
    if not os.path.exists(caminho_arquivo):
        print(f"Arquivo não encontrado: {caminho_arquivo}")
        return
    
    try:
        # Abre o arquivo e lê as linhas
        with open(caminho_arquivo, 'r', encoding='utf-8') as file:
            linhas = file.readlines()
            
        if not linhas:
            print("Arquivo vazio.")
            return
            
        print(f"Arquivo aberto com sucesso. Lendo {len(linhas)} linhas.")
        
        for i, linha in enumerate(linhas):
            linha = linha.strip()
            if not linha or linha.startswith('#'):
                continue

            partes = linha.split()
            if len(partes) > 0:
                smiles = partes[0]
                nome = " ".join(partes[1:]) if len(partes) > 1 else "Sem nome"
                print(f"Linha {i+1}: SMILES: {smiles} | Nome: {nome}")
                
                # Teste se o SMILES é válido
                mol = Chem.MolFromSmiles(smiles)
                if mol:
                    print(f"  - SMILES válido")
                else:
                    print(f"  - SMILES inválido")
    except Exception as e:
        print(f"Erro ao processar o arquivo: {str(e)}")

def d2(caminho_arquivo):
    print(f"Visualizando moléculas do arquivo: {caminho_arquivo}")
    
    # Verifica se o caminho do arquivo existe
    if not os.path.exists(caminho_arquivo):
        print(f"Arquivo não encontrado: {caminho_arquivo}")
        return
    
    try:
        # Abre o arquivo e lê as linhas
        with open(caminho_arquivo, 'r', encoding='utf-8') as file:
            linhas = file.readlines()
            
        if not linhas:
            print("Arquivo vazio.")
            return
            
        print(f"Arquivo aberto com sucesso. Processando {len(linhas)} linhas.")
        
        smiles_list = []
        nomes_list = []
        
        for i, linha in enumerate(linhas):
            linha = linha.strip()
            if not linha or linha.startswith('#'):
                continue

            partes = linha.split()
            if len(partes) > 0:
                smiles = partes[0]
                nome = " ".join(partes[1:]) if len(partes) > 1 else f"Molécula {i+1}"
                
                # Converte SMILES para molécula
                mol = Chem.MolFromSmiles(smiles)
                if mol:
                    mol.SetProp("_Name", nome)
                    smiles_list.append(mol)
                    nomes_list.append(nome)
                    print(f"Molécula adicionada: {nome}")
                else:
                    print(f"SMILES inválido ignorado: {smiles}")
        
        # Se houver moléculas válidas, desenha a grade
        if smiles_list:
            print(f"Desenhando grade com {len(smiles_list)} moléculas...")
            img = Draw.MolsToGridImage(
                smiles_list,
                molsPerRow=3,
                subImgSize=(250, 250),
                legends=nomes_list
            )
            display(img)
        else:
            print("Nenhuma molécula válida encontrada no arquivo.")
    except Exception as e:
        print(f"Erro ao processar o arquivo: {str(e)}")

def visualizar_smiles(entrada, nome="Molécula", salvar_sdf=False, caminho_sdf="mol_out.sdf"):
    """
    Visualiza uma molécula a partir de um SMILES string ou arquivo.
    
    Parâmetros:
    - entrada: String SMILES da molécula ou caminho para um arquivo .smi
    - nome: Nome opcional para a molécula (padrão: "Molécula")
    - salvar_sdf: Flag para salvar a molécula em formato SDF
    - caminho_sdf: Caminho para salvar o arquivo SDF
    """
    # Verifica se a entrada é um arquivo existente
    if os.path.exists(entrada) and entrada.endswith(".smi"):
        print(f"Detectado arquivo SMILES: {entrada}")
        try:
            with open(entrada, 'r', encoding='utf-8') as file:
                primeira_linha = None
                for linha in file:
                    linha = linha.strip()
                    if linha and not linha.startswith('#'):
                        primeira_linha = linha
                        break
                
                if primeira_linha:
                    partes = primeira_linha.split()
                    smiles = partes[0]
                    mol_nome = " ".join(partes[1:]) if len(partes) > 1 else nome
                    print(f"Usando primeira molécula do arquivo: {mol_nome}")
                    print(f"SMILES: {smiles}")
                else:
                    print("Arquivo vazio ou sem moléculas válidas.")
                    return
        except Exception as e:
            print(f"Erro ao ler arquivo: {e}")
            return
    else:
        # Considera a entrada como um SMILES diretamente
        smiles = entrada
        mol_nome = nome
    
    print(f"Visualizando molécula: {mol_nome}")
    
    try:
        # Converte SMILES para objeto molecular
        mol = Chem.MolFromSmiles(smiles)
        
        if not mol:
            print(f"SMILES inválido: {smiles}. Não foi possível criar a molécula.")
            return
        
        # Adiciona hidrogênios explícitos
        mol = Chem.AddHs(mol)
        
        # Gera conformação 3D
        try:
            AllChem.EmbedMolecule(mol, randomSeed=42)  # Otimiza a geometria
            AllChem.MMFFOptimizeMolecule(mol)  # Minimiza energia
        except Exception as e:
            print(f"Aviso: Problema na otimização 3D: {e}")
            print("Continuando com a visualização...")
        
        # Adiciona nome à molécula
        mol.SetProp("_Name", mol_nome)
        
        # Visualização 2D
        print("\nVisualização 2D:")
        img = Draw.MolToImage(mol, size=(400, 400))
        display(img)
        
        # Visualização 3D
        print("\nVisualização 3D (interativa):")
        # Converte molécula RDKit para formato PDB
        pdb_block = Chem.MolToPDBBlock(mol)
        
        # Cria visualização NGLView
        view = nv.show_text(pdb_block)
        view.clear_representations()
        view.add_ball_and_stick()
        view.center()
        display(view)

        # Salva a molécula em formato SDF (caso a flag seja True)
        if salvar_sdf:
            writer = Chem.SDWriter(caminho_sdf)
            writer.write(mol)
            writer.close()
            print(f"Molécula exportada como SDF em: {caminho_sdf}")
    except Exception as e:
        print(f"Erro ao visualizar SMILES: {e}")

def escolher_molecula(caminho_arquivo):
    """
    Permite escolher qual molécula do arquivo visualizar.
    """
    print(f"Escolhendo molécula do arquivo: {caminho_arquivo}")
    
    if not os.path.exists(caminho_arquivo):
        print(f"Arquivo não encontrado: {caminho_arquivo}")
        return
    
    try:
        # Lê todas as moléculas válidas do arquivo
        moleculas = []
        with open(caminho_arquivo, 'r', encoding='utf-8') as file:
            for i, linha in enumerate(file):
                linha = linha.strip()
                if linha and not linha.startswith('#'):
                    partes = linha.split()
                    if len(partes) > 0:
                        smiles = partes[0]
                        nome = " ".join(partes[1:]) if len(partes) > 1 else f"Molécula {i+1}"
                        
                        # Verifica se o SMILES é válido
                        mol = Chem.MolFromSmiles(smiles)
                        if mol:
                            moleculas.append((i, smiles, nome))
        
        if not moleculas:
            print("Nenhuma molécula válida encontrada no arquivo.")
            return
        
        # Exibe a lista de moléculas
        print(f"\nEncontradas {len(moleculas)} moléculas válidas:")
        for idx, (i, smiles, nome) in enumerate(moleculas):
            print(f"{idx+1}. {nome} - {smiles}")
        
        # Solicita a escolha do usuário
        while True:
            try:
                escolha = input("\nEscolha uma molécula (1-" + str(len(moleculas)) + ") ou 0 para cancelar: ")
                
                if escolha == "0":
                    print("Operação cancelada.")
                    return
                
                idx = int(escolha) - 1
                if idx < 0 or idx >= len(moleculas):
                    print(f"Escolha inválida. Digite um número entre 1 e {len(moleculas)}.")
                    continue
                
                # Visualiza a molécula escolhida
                _, smiles, nome = moleculas[idx]
                visualizar_smiles(smiles, nome)
                
                # Pergunta se deseja visualizar outra molécula
                continuar = input("\nDeseja visualizar outra molécula? (S/N): ").lower()
                if continuar != 's' and continuar != 'sim':
                    break
                else:
                    # Exibe novamente a lista de moléculas
                    print(f"\nEncontradas {len(moleculas)} moléculas válidas:")
                    for idx, (i, smiles, nome) in enumerate(moleculas):
                        print(f"{idx+1}. {nome} - {smiles}")
            except ValueError:
                print("Entrada inválida. Digite um número.")
            except Exception as e:
                print(f"Erro: {e}")
                break
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")

def converter_smi_para_sdf(arquivo_smi, saida_sdf="moleculas_out.sdf"):
    print(f"Convertendo arquivo {arquivo_smi} para SDF...")
    
    # Verifica se o caminho do arquivo existe
    if not os.path.exists(arquivo_smi):
        print(f"Arquivo não encontrado: {arquivo_smi}")
        return
    
    try:
        # Abre o arquivo e lê as linhas
        with open(arquivo_smi, 'r', encoding='utf-8') as file:
            linhas = file.readlines()
            
        if not linhas:
            print("Arquivo vazio.")
            return
            
        print(f"Arquivo aberto com sucesso. Processando {len(linhas)} linhas.")
        
        writer = Chem.SDWriter(saida_sdf)
        sucessos = 0
        falhas = 0
        
        for i, linha in enumerate(linhas):
            linha = linha.strip()
            if not linha or linha.startswith('#'):
                continue

            partes = linha.split()
            if len(partes) > 0:
                smiles = partes[0]
                nome = " ".join(partes[1:]) if len(partes) > 1 else f"Molécula {i+1}"
                
                print(f"Processando: {nome} - SMILES: {smiles}")
                
                # Converte SMILES para molécula
                mol = Chem.MolFromSmiles(smiles)
                if mol:
                    try:
                        mol = Chem.AddHs(mol)
                        AllChem.EmbedMolecule(mol, randomSeed=42)
                        AllChem.MMFFOptimizeMolecule(mol)
                        mol.SetProp("_Name", nome)
                        writer.write(mol)
                        sucessos += 1
                        print(f"  - Conversão bem-sucedida")
                    except Exception as e:
                        print(f"  - Erro na conversão 3D: {e}")
                        falhas += 1
                else:
                    print(f"  - SMILES inválido")
                    falhas += 1
        
        writer.close()
        print(f"Conversão concluída. Moléculas convertidas: {sucessos}, Falhas: {falhas}")
        print(f"Arquivo SDF salvo como: {saida_sdf}")
    except Exception as e:
        print(f"Erro ao converter arquivo: {e}")

def main():
    while True:
        print("\n--- Visualizador de Moléculas ---")
        print("1. Visualizar molécula por SMILES")
        print("2. Ler arquivo de SMILES")
        print("3. Converter arquivo .smi para .sdf")
        print("4. Visualizar todas as moléculas do arquivo SMILES")
        print("5. Escolher molécula específica do arquivo")
        print("6. Sair")
        
        try:
            escolha = input("Escolha uma opção (1-6): ")
            
            if escolha == '1':
                smiles = input("Digite o SMILES da molécula: ")
                nome = input("Digite o nome da molécula (opcional): ") or "Molécula"
                salvar = input("Deseja salvar a molécula como .sdf? (Sim/Não): ").lower()
                salvar_sdf = salvar.startswith("s")
                caminho_sdf = input("Digite o caminho para salvar o arquivo SDF (opcional): ") or "mol_out.sdf"
                visualizar_smiles(smiles, nome, salvar_sdf, caminho_sdf)
            
            elif escolha == '2':
                # Importante: use o caminho absoluto ou relativo correto
                caminho = input("Digite o caminho do arquivo de SMILES: ").strip()
                ler_arquivo_smiles(caminho)
            
            elif escolha == '3':
                # Importante: use o caminho absoluto ou relativo correto
                caminho = input("Digite o caminho do arquivo de SMILES: ").strip()
                saida = input("Digite o nome do arquivo de saída (.sdf): ").strip() or "moleculas_out.sdf"
                converter_smi_para_sdf(caminho, saida)
            
            elif escolha == '4':
                # Importante: use o caminho absoluto ou relativo correto
                caminho = input("Digite o caminho do arquivo de SMILES: ").strip()
                d2(caminho)
            
            elif escolha == '5':
                # Nova opção para escolher molécula específica
                caminho = input("Digite o caminho do arquivo de SMILES: ").strip()
                escolher_molecula(caminho)
            
            elif escolha == '6':
                print("Saindo...")
                break
            
            else:
                print("Opção inválida. Tente novamente.")
        except Exception as e:
            print(f"Erro inesperado: {e}")

# Função para usar como atalho em notebooks
def visu(entrada):
    """
    Função de conveniência para visualizar moléculas.
    Se a entrada é um arquivo SMILES, permite escolher qual molécula visualizar.
    Se a entrada é uma string SMILES, visualiza diretamente.
    """
    if os.path.exists(entrada) and entrada.endswith('.smi'):
        # Se for um arquivo SMILES, permite escolher qual molécula visualizar
        escolher_molecula(entrada)
    else:
        # Se não for um arquivo, trata como SMILES diretamente
        visualizar_smiles(entrada)

if __name__ == "__main__":
    main()
