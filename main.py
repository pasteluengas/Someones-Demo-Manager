someone = "Ri"

import osapi
import dataclasses
from nicegui import app, ui, events, logging

<<<<<<< HEAD
=======
app.add_static_files('/uploads', './uploads')

>>>>>>> aa87bb1 (Day 1)

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

<<<<<<< HEAD
=======
def delete_item(id):
    print("la idea es deletear a " + str(id['ID']))
    osapi.selectDemoById(id['ID']).delete()
    osapi.update_demos()
    #importante 
    ui.navigate.reload()

>>>>>>> aa87bb1 (Day 1)
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
<<<<<<< HEAD
=======


>>>>>>> aa87bb1 (Day 1)
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
<<<<<<< HEAD
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
=======
        # form
        with ui.expansion('Add new material', icon='add', group='left', value = False).classes('w-full'):
            with ui.card().classes('w-full shadow-2 lg:pa-md'):
                new_form_label = ui.label('Add new material').classes('text-h6 mb-2')
                
                new_form_name = ui.input(label='Name') \
                    .classes('w-full').props('outlined')

                new_form_type = ui.select(options=types, label='Materia type') \
                    .classes('w-full').props('outlined')

                new_form_notes = ui.textarea(label='Notes (Lyrics, chords, etc)') \
                    .classes('w-full') \
                    .props('outlined autogrow')

                new_form_upload = ui.upload(label='Upload Files', on_upload=handle_upload, auto_upload=True) \
                    .classes('w-full').props('flat bordered')

                ui.button('Save', on_click=newMaterialForum) \
                    .classes('w-full mt-4 py-4').props('color=primary icon=save')

        with ui.expansion('Viewer', icon='visibility', group='left', value = False).classes('w-full'):
            ui.label()
        
        
    #@ui.refreshable
    with ui.card().classes('w-full md:w-[60%] q-pa-none overflow-hidden') as updatable:
        table = []
        columns = [
            #{'name': 'ID', 'label': 'ID', 'field': 'ID', 'align': 'left'},
            {'name': 'name', 'label': 'Name', 'field': 'name', 'align': 'left'},
            {'name': 'type', 'label': 'Type', 'field': 'type'},
            {'name': 'view', 'label': 'View', 'field': 'view'},
            {'name': 'edit', 'label': 'Edit', 'field': 'edit'},
            {'name': 'delete', 'label': 'Delete', 'field': 'delete'},
        ]
        
        for getdemo in osapi.demos:
            table.append({'ID':getdemo.id, 'type': types[getdemo.type], 'name': getdemo.name})
        with ui.table(columns = columns,rows=table).props('flat bordered').classes("w-full") as uitable:
            uitable.add_slot("body-cell-delete", '''
            <q-td :props="props">
                        <q-btn 
                            flat 
                            round 
                            color="dark" 
                            icon="delete" 
                            @click="$parent.$emit('delete', props)"
                        />
                    </q-td>
            ''')
            uitable.add_slot("body-cell-edit", '''
            <q-td :props="props">
                        <q-btn 
                            flat 
                            round 
                            color="dark" 
                            icon="edit" 
                            @click="$parent.$emit('edit', props)"
                        />
                    </q-td>
            ''')
            uitable.add_slot("body-cell-view", '''
            <q-td :props="props">
                        <q-btn 
                            flat 
                            round 
                            color="dark" 
                            icon="visibility" 
                            @click="$parent.$emit('view', props)"
                        />
                    </q-td>
            ''')

            
            uitable.on('delete', lambda val: delete_item(val.args['row']))
            uitable.on('edit', lambda val: print(val.args['row']))
            uitable.on('view', lambda val: print(val.args['row']))
            
        #table.on('action', lambda msg: print(msg))
>>>>>>> aa87bb1 (Day 1)

ui.run(port=8081, reload=False)
    
