someone = "Ri"

import osapi
import dataclasses
from nicegui import app, ui, events, logging


osapi.init()
osapi.update_demos()

types = {
    "inst": "Instrumental",
    "demo": "Demo",
    "lyr": "Lyrics",
    "riff": "Riff",
    "phra": "Phrase",
    "idea": "Idea"
}

tmpfiles = []
async def handle_upload(e):
    #print(str(e.file.read()), flush=True)  
    #tmpfiles.append({"name": e.file.name, "content": e.file.read()}) 
    await e.file.save(".tmp/" + str(e.file.name))
    tmpfiles.append(str(e.file.name))

def newMaterialForum(): 
    material_name = new_form_name.value
    material_type = new_form_type.value
    try:
        newMaterial = osapi.newDemo(material_type, material_name)
    except Exception as e:
        ui.label("Error: " + str(e))
        return 1
    osapi.update_demos()
    #ui.label("id del nuevomaterial: " + str(newMaterial))

    if new_form_notes.value:
       osapi.selectDemoById(newMaterial).add_note(new_form_notes.value)

    if new_form_name.value:
        osapi.movFromTmp(tmpfiles, osapi.selectDemoById(newMaterial).path)
        osapi.emtpyTmp()
### Front end starts

#<head>
app.colors(primary='#B32100', brand='#FF6347', dark='#121212')

#<header>
ui.page_title(someone + "'s Demo Manager")

with ui.header(elevated=True).classes('items-center justify-between bg-primary text-white q-pa-md'):
    with ui.row().classes('items-center gap-4'):
        ui.icon('folder_shared', size='2em')
        ui.label(someone + "'s Demo Manager").classes('text-h4 font-bold')
        ui.label('LAN website: ' + str(osapi.getURL(app.urls))).classes('font-bold')

#<elresto>
ip = ui.label("Visite esta mierda en: " + str(osapi.getURL(app.urls)) + " (solo funciona en la red local)")

with ui.row().classes('w-full no-wrap items-start md:flex-row flex-col'):
    with ui.card().classes('w-full md:w-[40%] q-pa-md'):
        #izq
        #form
        with ui.card().classes('w-full shadow-2 lg:pa-md'):
            ui.label('Add new material').classes('text-h6 mb-2')
            
            new_form_name = ui.input(label='Name') \
                .classes('w-full').props('outlined')

            new_form_type = ui.select(options=types, label='Materia type') \
                .classes('w-full').props('outlined')

            new_form_notes = ui.textarea(label='Notes (Lyrics, chords, etc)') \
                .classes('w-full') \
                .props('outlined autogrow')

            ui.upload(label='Upload Files', on_upload=handle_upload, auto_upload=True) \
                .classes('w-full').props('flat bordered')

            ui.button('Save', on_click=newMaterialForum) \
                .classes('w-full mt-4 py-4').props('color=primary icon=save')
        
        
    with ui.card().classes('w-full md:w-[60%] q-pa-none overflow-hidden'):
        table = []
        for getdemo in osapi.demos:
            table.append({'ID':getdemo.id, 'type': types[getdemo.type], 'name': getdemo.name})
        ui.table(rows=table).props('flat bordered').classes("w-full")

ui.run(port=8081, reload=False)
    
