from datetime import datetime

class UnirvestagiosSystem:
    def __init__(self):
        # Listas para armazenar dados localmente
        self.usuarios = []
        self.estagios = []
        self.candidaturas = []
        self.proximo_id = 1
    
    def gerar_id(self):
        """Gera um ID único"""
        id_atual = self.proximo_id
        self.proximo_id += 1
        return id_atual
    
    def cadastrar_usuario(self, nome, email, senha, tipo, telefone=None, curso=None, periodo=None):
        """Cadastra um novo usuário (estudante ou empresa)"""
        # Verifica se email já existe
        for usuario in self.usuarios:
            if usuario['email'] == email:
                return False, "E-mail já cadastrado no sistema!"
        
        novo_usuario = {
            'id': self.gerar_id(),
            'nome': nome,
            'email': email,
            'senha': senha,
            'tipo': tipo,
            'telefone': telefone,
            'curso': curso,
            'periodo': periodo,
            'data_cadastro': datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        
        self.usuarios.append(novo_usuario)
        return True, "Usuário cadastrado com sucesso!"
    
    def login(self, email, senha):
        """Realiza login do usuário"""
        for usuario in self.usuarios:
            if usuario['email'] == email and usuario['senha'] == senha:
                return True, {
                    'id': usuario['id'],
                    'nome': usuario['nome'],
                    'tipo': usuario['tipo']
                }
        return False, "E-mail ou senha incorretos!"
    
    def publicar_estagio(self, empresa_id, titulo, descricao, area, requisitos, 
                        salario=None, carga_horaria=None, local=None, tipo_estagio=None):
        """Permite que empresas publiquem vagas de estágio"""
        novo_estagio = {
            'id': self.gerar_id(),
            'empresa_id': empresa_id,
            'titulo': titulo,
            'descricao': descricao,
            'area': area,
            'requisitos': requisitos,
            'salario': salario,
            'carga_horaria': carga_horaria,
            'local': local,
            'tipo_estagio': tipo_estagio,
            'data_publicacao': datetime.now().strftime("%d/%m/%Y %H:%M"),
            'ativo': True
        }
        
        self.estagios.append(novo_estagio)
        return True, "Estágio publicado com sucesso!"
    
    def buscar_estagios(self, area=None, local=None, tipo_estagio=None):
        """Busca estágios disponíveis com filtros opcionais"""
        estagios_encontrados = []
        
        for estagio in self.estagios:
            if not estagio['ativo']:
                continue
            
            # Aplica filtros se fornecidos
            if area and area.lower() not in estagio['area'].lower():
                continue
            
            if local and estagio['local'] and local.lower() not in estagio['local'].lower():
                continue
            
            if tipo_estagio and estagio['tipo_estagio'] != tipo_estagio:
                continue
            
            # Busca nome da empresa
            empresa_nome = "Empresa não encontrada"
            for usuario in self.usuarios:
                if usuario['id'] == estagio['empresa_id']:
                    empresa_nome = usuario['nome']
                    break
            
            estagio_completo = estagio.copy()
            estagio_completo['empresa_nome'] = empresa_nome
            estagios_encontrados.append(estagio_completo)
        
        return estagios_encontrados
    
    def candidatar_estagio(self, estudante_id, estagio_id):
        """Permite que estudantes se candidatem a estágios"""
        # Verifica se já existe candidatura
        for candidatura in self.candidaturas:
            if candidatura['estudante_id'] == estudante_id and candidatura['estagio_id'] == estagio_id:
                return False, "Você já se candidatou a este estágio!"
        
        nova_candidatura = {
            'id': self.gerar_id(),
            'estudante_id': estudante_id,
            'estagio_id': estagio_id,
            'data_candidatura': datetime.now().strftime("%d/%m/%Y %H:%M"),
            'status': 'pendente'
        }
        
        self.candidaturas.append(nova_candidatura)
        return True, "Candidatura realizada com sucesso!"
    
    def listar_candidaturas_empresa(self, empresa_id):
        """Lista candidaturas para os estágios de uma empresa"""
        candidaturas_empresa = []
        
        for candidatura in self.candidaturas:
            # Busca o estágio
            estagio = None
            for est in self.estagios:
                if est['id'] == candidatura['estagio_id'] and est['empresa_id'] == empresa_id:
                    estagio = est
                    break
            
            if not estagio:
                continue
            
            # Busca dados do estudante
            estudante = None
            for usuario in self.usuarios:
                if usuario['id'] == candidatura['estudante_id']:
                    estudante = usuario
                    break
            
            if estudante:
                candidatura_completa = {
                    'candidatura_id': candidatura['id'],
                    'estagio_titulo': estagio['titulo'],
                    'estudante_nome': estudante['nome'],
                    'estudante_email': estudante['email'],
                    'estudante_curso': estudante.get('curso', 'Não informado'),
                    'estudante_periodo': estudante.get('periodo', 'Não informado'),
                    'data_candidatura': candidatura['data_candidatura'],
                    'status': candidatura['status']
                }
                candidaturas_empresa.append(candidatura_completa)
        
        return candidaturas_empresa
    
    def meus_estagios_publicados(self, empresa_id):
        """Lista estágios publicados por uma empresa"""
        estagios_empresa = []
        
        for estagio in self.estagios:
            if estagio['empresa_id'] == empresa_id:
                estagios_empresa.append(estagio)
        
        return estagios_empresa
    
    def minhas_candidaturas(self, estudante_id):
        """Lista candidaturas de um estudante"""
        candidaturas_estudante = []
        
        for candidatura in self.candidaturas:
            if candidatura['estudante_id'] == estudante_id:
                # Busca dados do estágio
                estagio = None
                for est in self.estagios:
                    if est['id'] == candidatura['estagio_id']:
                        estagio = est
                        break
                
                if estagio:
                    # Busca nome da empresa
                    empresa_nome = "Empresa não encontrada"
                    for usuario in self.usuarios:
                        if usuario['id'] == estagio['empresa_id']:
                            empresa_nome = usuario['nome']
                            break
                    
                    candidatura_completa = {
                        'candidatura_id': candidatura['id'],
                        'estagio_titulo': estagio['titulo'],
                        'empresa_nome': empresa_nome,
                        'data_candidatura': candidatura['data_candidatura'],
                        'status': candidatura['status']
                    }
                    candidaturas_estudante.append(candidatura_completa)
        
        return candidaturas_estudante

def main():
    sistema = UnirvestagiosSystem()
    usuario_logado = None
    
    print("=== SISTEMA UNIRV ESTÁGIOS ===")
    print("Sistema iniciado com dados locais!")
    
    while True:
        if not usuario_logado:
            print(f"\n{'='*40}")
            print("1. Cadastrar usuário")
            print("2. Fazer login")
            print("3. Buscar estágios (público)")
            print("0. Sair")
            print(f"{'='*40}")
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == "1":
                print(f"\n{'-'*30}")
                print("CADASTRO DE USUÁRIO")
                print(f"{'-'*30}")
                nome = input("Nome: ")
                email = input("E-mail: ")
                senha = input("Senha: ")
                
                print("\nTipo de usuário:")
                print("1. Estudante")
                print("2. Empresa")
                tipo_opcao = input("Escolha (1 ou 2): ")
                
                if tipo_opcao not in ['1', '2']:
                    print("Opção inválida!")
                    continue
                
                tipo = "estudante" if tipo_opcao == "1" else "empresa"
                
                telefone = input("Telefone (opcional): ") or None
                
                if tipo == "estudante":
                    curso = input("Curso: ") or None
                    try:
                        periodo_input = input("Período (opcional): ")
                        periodo = int(periodo_input) if periodo_input else None
                    except ValueError:
                        periodo = None
                else:
                    curso = None
                    periodo = None
                
                sucesso, mensagem = sistema.cadastrar_usuario(nome, email, senha, tipo, telefone, curso, periodo)
                print(f"\n✓ {mensagem}" if sucesso else f"\n✗ {mensagem}")
            
            elif opcao == "2":
                print(f"\n{'-'*30}")
                print("LOGIN")
                print(f"{'-'*30}")
                email = input("E-mail: ")
                senha = input("Senha: ")
                
                sucesso, resultado = sistema.login(email, senha)
                if sucesso:
                    usuario_logado = resultado
                    print(f"\n✓ Bem-vindo(a), {usuario_logado['nome']}!")
                else:
                    print(f"\n✗ {resultado}")
            
            elif opcao == "3":
                print(f"\n{'-'*30}")
                print("BUSCAR ESTÁGIOS")
                print(f"{'-'*30}")
                area = input("Área (opcional): ") or None
                local = input("Local (opcional): ") or None
                
                estagios = sistema.buscar_estagios(area=area, local=local)
                
                if estagios:
                    print(f"\n🎯 {len(estagios)} estágio(s) encontrado(s):")
                    for i, estagio in enumerate(estagios, 1):
                        print(f"\n{'-'*40}")
                        print(f"#{i} - {estagio['titulo']}")
                        print(f"Empresa: {estagio['empresa_nome']}")
                        print(f"Área: {estagio['area']}")
                        print(f"Local: {estagio['local'] or 'Não informado'}")
                        print(f"Salário: R$ {estagio['salario'] or 'A combinar'}")
                        print(f"Carga Horária: {estagio['carga_horaria'] or 'Não informado'}")
                        print(f"Descrição: {estagio['descricao']}")
                        print(f"Requisitos: {estagio['requisitos']}")
                        print(f"Data: {estagio['data_publicacao']}")
                else:
                    print("\n❌ Nenhum estágio encontrado.")
            
            elif opcao == "0":
                print("\n👋 Obrigado por usar o sistema!")
                break
            
            else:
                print("\n❌ Opção inválida!")
        
        else:
            # Menu para usuário logado
            if usuario_logado['tipo'] == 'empresa':
                print(f"\n{'='*50}")
                print(f"MENU EMPRESA - {usuario_logado['nome']}")
                print(f"{'='*50}")
                print("1. Publicar novo estágio")
                print("2. Meus estágios publicados")
                print("3. Ver candidaturas")
                print("4. Logout")
                
                opcao = input("\nEscolha uma opção: ")
                
                if opcao == "1":
                    print(f"\n{'-'*30}")
                    print("PUBLICAR ESTÁGIO")
                    print(f"{'-'*30}")
                    titulo = input("Título da vaga: ")
                    descricao = input("Descrição: ")
                    area = input("Área: ")
                    requisitos = input("Requisitos: ")
                    
                    try:
                        salario_input = input("Salário (0 ou vazio para não informar): ")
                        salario = float(salario_input) if salario_input and salario_input != '0' else None
                    except ValueError:
                        salario = None
                    
                    carga_horaria = input("Carga horária (ex: 20h/semana): ") or None
                    local = input("Local: ") or None
                    
                    print("\nTipo de estágio:")
                    print("1. Obrigatório")
                    print("2. Não obrigatório")
                    tipo_opcao = input("Escolha (1 ou 2): ")
                    tipo_estagio = "obrigatorio" if tipo_opcao == "1" else "nao_obrigatorio"
                    
                    sucesso, mensagem = sistema.publicar_estagio(
                        usuario_logado['id'], titulo, descricao, area, requisitos,
                        salario, carga_horaria, local, tipo_estagio
                    )
                    print(f"\n✓ {mensagem}" if sucesso else f"\n✗ {mensagem}")
                
                elif opcao == "2":
                    estagios = sistema.meus_estagios_publicados(usuario_logado['id'])
                    
                    if estagios:
                        print(f"\n📋 Seus estágios publicados ({len(estagios)}):")
                        for i, estagio in enumerate(estagios, 1):
                            status = "🟢 Ativo" if estagio['ativo'] else "🔴 Inativo"
                            print(f"\n{'-'*40}")
                            print(f"#{i} - {estagio['titulo']} ({status})")
                            print(f"Área: {estagio['area']}")
                            print(f"Salário: R$ {estagio['salario'] or 'A combinar'}")
                            print(f"Data: {estagio['data_publicacao']}")
                    else:
                        print("\n❌ Você ainda não publicou nenhum estágio.")
                
                elif opcao == "3":
                    candidaturas = sistema.listar_candidaturas_empresa(usuario_logado['id'])
                    
                    if candidaturas:
                        print(f"\n👥 Candidaturas recebidas ({len(candidaturas)}):")
                        for i, cand in enumerate(candidaturas, 1):
                            status_emoji = "⏳" if cand['status'] == 'pendente' else "✅" if cand['status'] == 'aceito' else "❌"
                            print(f"\n{'-'*40}")
                            print(f"#{i} - {cand['estagio_titulo']}")
                            print(f"Candidato: {cand['estudante_nome']}")
                            print(f"E-mail: {cand['estudante_email']}")
                            print(f"Curso: {cand['estudante_curso']}")
                            print(f"Período: {cand['estudante_periodo']}")
                            print(f"Data: {cand['data_candidatura']}")
                            print(f"Status: {status_emoji} {cand['status'].title()}")
                    else:
                        print("\n❌ Nenhuma candidatura recebida ainda.")
                
                elif opcao == "4":
                    usuario_logado = None
                    print("\n👋 Logout realizado com sucesso!")
                
                else:
                    print("\n❌ Opção inválida!")
            
            else:  # estudante
                print(f"\n{'='*50}")
                print(f"MENU ESTUDANTE - {usuario_logado['nome']}")
                print(f"{'='*50}")
                print("1. Buscar estágios")
                print("2. Candidatar-se a estágio")
                print("3. Minhas candidaturas")
                print("4. Logout")
                
                opcao = input("\nEscolha uma opção: ")
                
                if opcao == "1":
                    print(f"\n{'-'*30}")
                    print("BUSCAR ESTÁGIOS")
                    print(f"{'-'*30}")
                    area = input("Área (opcional): ") or None
                    local = input("Local (opcional): ") or None
                    
                    estagios = sistema.buscar_estagios(area=area, local=local)
                    
                    if estagios:
                        print(f"\n🎯 {len(estagios)} estágio(s) encontrado(s):")
                        for i, estagio in enumerate(estagios, 1):
                            print(f"\n{'-'*40}")
                            print(f"ID: {estagio['id']} - {estagio['titulo']}")
                            print(f"Empresa: {estagio['empresa_nome']}")
                            print(f"Área: {estagio['area']}")
                            print(f"Local: {estagio['local'] or 'Não informado'}")
                            print(f"Salário: R$ {estagio['salario'] or 'A combinar'}")
                            print(f"Carga Horária: {estagio['carga_horaria'] or 'Não informado'}")
                            print(f"Descrição: {estagio['descricao']}")
                    else:
                        print("\n❌ Nenhum estágio encontrado.")
                
                elif opcao == "2":
                    try:
                        estagio_id = int(input("\nDigite o ID do estágio para se candidatar: "))
                        sucesso, mensagem = sistema.candidatar_estagio(usuario_logado['id'], estagio_id)
                        print(f"\n✓ {mensagem}" if sucesso else f"\n✗ {mensagem}")
                    except ValueError:
                        print("\n❌ ID inválido!")
                
                elif opcao == "3":
                    candidaturas = sistema.minhas_candidaturas(usuario_logado['id'])
                    
                    if candidaturas:
                        print(f"\n📋 Suas candidaturas ({len(candidaturas)}):")
                        for i, cand in enumerate(candidaturas, 1):
                            status_emoji = "⏳" if cand['status'] == 'pendente' else "✅" if cand['status'] == 'aceito' else "❌"
                            print(f"\n{'-'*40}")
                            print(f"#{i} - {cand['estagio_titulo']}")
                            print(f"Empresa: {cand['empresa_nome']}")
                            print(f"Data: {cand['data_candidatura']}")
                            print(f"Status: {status_emoji} {cand['status'].title()}")
                    else:
                        print("\n❌ Você ainda não se candidatou a nenhum estágio.")
                
                elif opcao == "4":
                    usuario_logado = None
                    print("\n👋 Logout realizado com sucesso!")
                
                else:
                    print("\n❌ Opção inválida!")

if __name__ == "__main__":
    main()