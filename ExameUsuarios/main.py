import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from conexionBD import ConexionBD

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table


class Exame(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Exame 15-04-2023")
        self.set_border_width(10)

        builder = Gtk.Builder()
        builder.add_from_file("Usuarios.glade")

        usuarios_frm = builder.get_object("usuarios_frm")
        self.dni_cbt = builder.get_object("dni_cbt")
        self.nome_label = builder.get_object("nome_entry")

        self.db = ConexionBD("perfisUsuarios.bd")
        self.db.conectaBD()
        self.db.creaCursor()

        query_dni = "select dni from usuarios"
        dnis = self.db.consultaSenParametros(query_dni)

        for i, dni in enumerate(dnis):
            self.dni_cbt.append_text(dnis[i][0])
            print(f"Index {i}: DNI {dni}")


        self.dni_cbt.connect("changed", self.dni_cbt_changed)

        perfis_frm = Gtk.Frame(label="Perfís usuario")
        model = Gtk.ListStore(str, str, str)
        self.perfis_trv = Gtk.TreeView(model=model)

        crt = Gtk.CellRendererText()
        col1 = Gtk.TreeViewColumn("Nome perfil", crt, text=0)
        col2 = Gtk.TreeViewColumn("Descricion", crt, text=1)
        col3 = Gtk.TreeViewColumn("Permisos", crt, text=2)

        self.perfis_trv.append_column(col1)
        self.perfis_trv.append_column(col2)
        self.perfis_trv.append_column(col3)

        caixaVBotons = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        btnNovo = Gtk.Button(label="Novo")
        btnEditar = Gtk.Button(label="Editar")
        btnBorrar = Gtk.Button(label="Borrar")

        caixaVBotons.add(btnNovo)
        caixaVBotons.add(btnEditar)
        caixaVBotons.add(btnBorrar)

        hbox_frm = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        hbox_frm.add(self.perfis_trv)
        hbox_frm.add(caixaVBotons)
        perfis_frm.add(hbox_frm)

        lblNomePerfil = Gtk.Label(label="Nome perfíl")
        txtNomePerfil = Gtk.Entry()
        lblPermisos = Gtk.Label(label="Permisos")

        btm_h_box1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        btm_h_box1.add(lblNomePerfil)
        btm_h_box1.add(txtNomePerfil)
        btm_h_box1.add(lblPermisos)

        lblDescripcionPerfil = Gtk.Label(label="Descripción")
        txtDescripcionPerfil = Gtk.Entry()
        cmbPermisos = Gtk.ComboBox()

        btm_h_box2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        btm_h_box2.add(lblDescripcionPerfil)
        btm_h_box2.add(txtDescripcionPerfil)
        btm_h_box2.add(cmbPermisos)

        pdf_btn = Gtk.Button(label="Generar PDF")
        pdf_btn.connect("clicked", self.on_pdf_clicked)

        main_v_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_v_box.add(usuarios_frm)
        main_v_box.add(perfis_frm)


        main_v_box.add(pdf_btn)

        self.add(main_v_box)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def dni_cbt_changed(self, cbt):
        dni = self.dni_cbt.get_active_text()

        nome_query = "select nome from usuarios where dni=?"
        nome = self.db.consultaConParametros(nome_query, dni)
        self.nome_label.set_text(nome[0][0])

        permiso_idPerfil = "select idPerfil, permiso from perfisUsuario where dniUsuario=?"
        perfis_query = "select nomePerfil, descricion from perfis where idPefil=?"

        permiso_idPerfil = self.db.consultaConParametros(permiso_idPerfil, dni)
        datos_perfil = self.db.consultaConParametros(perfis_query, permiso_idPerfil[0][0])
        print(datos_perfil[0][0], datos_perfil[0][1], permiso_idPerfil[0][0])
        print(datos_perfil)
        print(permiso_idPerfil)

        model = self.perfis_trv.get_model()
        model.clear()
        permisos = ""
        if permiso_idPerfil[0][1] == 0:
            permisos = "Sen permisos"
        if permiso_idPerfil[0][1] == 1:
            permisos = "Lectura"
        if permiso_idPerfil[0][1] == 2:
            permisos = "Lectura y escritura"

        model.append([datos_perfil[0][0], datos_perfil[0][1], permisos])

    def on_pdf_clicked(self, row):
        dni = self.dni_cbt.get_active_text()

        doc = SimpleDocTemplate("Usuarios.pdf", pagesize=A4)

        query_email = "select nome, correoe from usuarios where dni=?"
        datos_email = self.db.consultaConParametros(query_email, dni)

        data = ([("Nome", "DNI", "Email")])

        for row in datos_email:
            print(row[0])
            data.append([row[0], dni, row[1]])
            print(f"Row{row},Dni{dni}")

        table = Table(data)
        doc.build([table])


if __name__ == "__main__":
    Exame()
    Gtk.main()
