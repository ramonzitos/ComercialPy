#!/usr/bin/env python
# coding: iso-8859-1
# ComercialPy - Licensiado sob GPL2.
# Versão: 0.1
from gi.repository import Gtk
from pysqlite2 import dbapi2 as sqlite
global con, cursor
con = sqlite.connect("comercialpy.db")
cursor = con.cursor()

def verify_camps(self):
  dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Erro!")
  dialog.format_secondary_text("Preencha corretamente todos os campos")
  for i in range(1, 5):
    if eval("self.entry%i.get_text()" % i) == "":
      dialog.run()
      dialog.destroy()
      return False
  try:
    float(".".join(self.entry4.get_text().split(",")))
    int(self.entry3.get_text())
  except ValueError:
    dialog.run()
    dialog.destroy()
    return False
  return True

def get_camps(self):
  preco = float(".".join(self.entry4.get_text().split(",")))
  quantidade = int(self.entry3.get_text())
  nome = self.entry1.get_text().upper()
  codigo = self.entry2.get_text().upper()
  return (nome, codigo, quantidade, preco)

class EditWindow(Gtk.Window):
  def __init__(self, prod_id):
    global con, cursor
    self.prod_id = prod_id
    Gtk.Window.__init__(self, title="Editar - ComercialPy")
    cursor.execute("select * from produtos where id=?", (self.prod_id,))
    prod = cursor.fetchone()
    # - Boxes
    self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    for i in range(1, 6):
      exec("self.hbox%i = Gtk.Box()" % i)
    # - Elementos
    j = 0
    for i in ["Nome:", "Codigo:", "Quantidade:", "Preco: R$ "]:
      j = j + 1
      exec("self.label%i = Gtk.Label(\"%s\")" % (j, i))
    del j
    for i in range(1, 5):
      exec("self.entry%i = Gtk.Entry()" % i)
      exec("self.entry%i.set_text(\"%s\")" % (i, prod[i]))
    self.bt_svr = Gtk.Button(label="Salvar", stock=Gtk.STOCK_SAVE)
    self.bt_ccl = Gtk.Button(label="Cancelar", stock=Gtk.STOCK_CANCEL)
    # - Ligando boxes aos elementos
    # -- Hbox's 1, 2, 3 e 4.
    for i in range(1, 5):
      exec("self.hbox%i.pack_start(self.label%i, False, False, 0)" % (i, i))
      exec("self.hbox%i.pack_start(self.entry%i, True, True, 0)" % (i, i))
      exec("self.vbox.pack_start(self.hbox%i, False, False, 0)" % i)
    self.hbox5.pack_start(self.bt_svr, True, True, 0)
    self.hbox5.pack_start(self.bt_ccl, True, True, 0)
    self.vbox.pack_start(self.hbox5, False, False, 0)
    self.add(self.vbox)
    # Signals
    self.bt_svr.connect("clicked", self.on_bt_svr_clicked)
    self.bt_ccl.connect("clicked", self.on_bt_ccl_clicked)
  def on_bt_svr_clicked(self, widget):
    global con, cursor
    if verify_camps(self) == False: return
    cursor.execute("UPDATE produtos SET nome=?, codigo=?, quantidade=?, preco=? WHERE id=?", get_camps(self) + (self.prod_id,))
    con.commit()
    dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Informação!")
    dialog.format_secondary_text("Salvo!")
    dialog.run()
    dialog.destroy()
    return
  def on_bt_ccl_clicked(self, widget):
    self.destroy()

class InsertWindow(Gtk.Window):
  def __init__(self):
    global con, cursor
    Gtk.Window.__init__(self, title="Inserir - ComercialPy")
    # - Boxes
    self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    for i in range(1, 6):
      exec("self.hbox%i = Gtk.Box()" % i)
    # - Elementos
    j = 0
    for i in ["Nome:", "Codigo:", "Quantidade:", "Preco: R$ "]:
      j = j + 1
      exec("self.label%i = Gtk.Label(\"%s\")" % (j, i))
    del j
    for i in range(1, 5):
      exec("self.entry%i = Gtk.Entry()" % i)
    self.bt_crt = Gtk.Button(label="OK", stock=Gtk.STOCK_SAVE)
    self.bt_ccl = Gtk.Button(label="Cancelar", stock=Gtk.STOCK_CANCEL)
    # - Ligando boxes aos elementos
    # -- Hbox's 1, 2. e 3.
    for i in range(1, 5):
      exec("self.hbox%i.pack_start(self.label%i, False, False, 0)" % (i, i))
      exec("self.hbox%i.pack_start(self.entry%i, True, True, 0)" % (i, i))
      exec("self.vbox.pack_start(self.hbox%i, False, False, 0)" % i)
    self.hbox5.pack_start(self.bt_crt, True, True, 0)
    self.hbox5.pack_start(self.bt_ccl, True, True, 0)
    self.vbox.pack_start(self.hbox5, False, False, 0)
    self.add(self.vbox)
    # Signals
    self.bt_crt.connect("clicked", self.on_bt_crt_clicked)
  def on_bt_crt_clicked(self, widget):
    global con, cursor
    if verify_camps(self) == False: return
    cursor.execute("INSERT INTO produtos(nome, codigo, quantidade, preco) VALUES(?, ?, ?, ?)", get_camps(self))
    con.commit()
    dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Informação!")
    dialog.format_secondary_text("Salvo!")
    dialog.run()
    dialog.destroy()
    return
    
class MainWindow(Gtk.Window):
  def __init__(self):
    global con, cursor
    Gtk.Window.__init__(self, title="ComercialPy")
    # - Boxes
    self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    self.add(self.vbox)
    self.hbox1 = Gtk.Box()
    self.hbox2 = Gtk.Box()
    self.vbox.pack_start(self.hbox1, False, False, 0)
    self.vbox.pack_start(self.hbox2, False, False, 0)
    # - Elementos
    # -- Hbox1
    self.bt_ins = Gtk.Button(label="Inserir", stock=Gtk.STOCK_ADD)
    self.bt_edt = Gtk.Button(label="Editar", stock=Gtk.STOCK_EDIT)
    self.bt_del = Gtk.Button(label="Apagar", stock=Gtk.STOCK_REMOVE)
    # -- Hbox2
    self.entry_srh = Gtk.Entry()
    self.cb_lst_srh = Gtk.ListStore(str, str)
    self.cb_lst_srh.append(["id", "ID"])
    self.cb_lst_srh.append(["nome", "Nome"])
    self.cb_lst_srh.append(["codigo", "Codigo"])
    self.cb_lst_srh.append(["preco", "Preco"])
    self.cb_render = Gtk.CellRendererText()
    self.cb_srh = Gtk.ComboBox.new_with_model(self.cb_lst_srh)
    self.cb_srh.pack_start(self.cb_render, True)
    self.cb_srh.add_attribute(self.cb_render, "text", 1)
    self.bt_srh = Gtk.Button(label="Pesquisar", stock=Gtk.STOCK_FIND)
    # -- Tree
    self.list_store = Gtk.ListStore(int, str, str, int, str) # ID, Nome, Codigo, Quantidade, Preco
    self.tree = Gtk.TreeView(model=self.list_store)
    self.selection = self.tree.get_selection()
    self.scw = Gtk.ScrolledWindow()
    self.scw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
    self.scw.add(self.tree)
    # --- Criando CellRenderers e Colunas
    j = 0
    for i in ["id", "nome", "codigo", "quantidade", "preco"]:
      exec("render_%s = Gtk.CellRendererText()" % i)
      exec("coluna_%s = Gtk.TreeViewColumn(\"%s\", render_%s, text = %i)" % (i, i.capitalize(), i, j))
      j = j + 1
      exec("self.tree.append_column(coluna_%s)" % i)
    del j
    # - Ligando Boxes aos Elementos
    self.vbox.pack_start(self.scw, True, True, 0)
    # -- Hbox1
    self.hbox1.pack_start(self.bt_ins, True, True, 0)
    self.hbox1.pack_start(self.bt_edt, True, True, 0)
    self.hbox1.pack_start(self.bt_del, True, True, 0)
    # -- Hbox2
    self.hbox2.pack_start(self.entry_srh, True, True, 0)
    self.hbox2.pack_start(self.cb_srh, False, False, 0)
    self.hbox2.pack_start(self.bt_srh, False, False, 0)
    # - Criando signals
    self.bt_ins.connect("clicked", self.on_bt_ins_clicked)
    self.bt_srh.connect("clicked", self.on_bt_srh_clicked)
    self.bt_edt.connect("clicked", self.on_bt_edt_clicked)
    self.bt_del.connect("clicked", self.on_bt_del_clicked)
  def on_bt_ins_clicked(self, widget):
    win = InsertWindow()
    win.show_all()
  def on_bt_srh_clicked(self, widget):
    global con, cursor
    text = self.entry_srh.get_text()
    treeiter = self.cb_srh.get_active_iter()
    if text == "" or treeiter == None: return
    model = self.cb_srh.get_model()
    choice = model[treeiter][0]
    cursor.execute("select * from produtos where %s LIKE ?" % choice, ('%' + text + '%',))
    self.list_store.clear()
    for i in cursor:
      i = list(i)
      i[-1] = ",".join(("R$ %.2f" % i[-1]).split("."))
      self.list_store.append(i)
  def on_bt_edt_clicked(self, widget):
    model, treeiter = self.selection.get_selected()
    if treeiter != None:
      win = EditWindow(model[treeiter][0])
      win.show_all()
  def on_bt_del_clicked(self, widget):
    global con, cursor
    model, treeiter = self.selection.get_selected()
    if treeiter != None:
      dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.YES_NO, "Tem certeza?")
      dialog.format_secondary_text("Deseja mesmo excluir \"%s\"?" % model[treeiter][1])
      resposta = dialog.run()
      dialog.destroy()
      if resposta == Gtk.ResponseType.YES:
        cursor.execute("delete from produtos where id=?", (model[treeiter][0],))
        con.commit()
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Informação")
        dialog.format_secondary_text("Excluido com sucesso!")
        dialog.run()
        dialog.destroy()
    return

if __name__ == "__main__":
  win = MainWindow()
  win.connect("delete-event", Gtk.main_quit)
  win.show_all()
  Gtk.main()
