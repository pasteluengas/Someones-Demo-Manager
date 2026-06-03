someone = "Ri"

import osapi
import os
import dataclasses
from nicegui import app, ui, events, logging

app.add_static_files('/uploads', './uploads')


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

icontypes = {
    "inst": "piano",
    "demo": "album",
    "lyr": "lyrics",
    "riff": "filter_retrolux",
    "phra": "quick_phrases",
    "idea": "emoji_objects"
}

tmpfiles = []
async def handle_upload(e):
    await e.file.save(".tmp/" + str(e.file.name))
    tmpfiles.append(str(e.file.name))

def delete_item(id):
    osapi.selectDemoById(id['ID']).delete()
    osapi.update_demos()
    #importante 
    ui.navigate.reload()

def newMaterialForum(): 
    material_name = new_form_name.value
    material_type = new_form_type.value
    try:
        newMaterial = osapi.newDemo(material_type, material_name)
    except Exception as e:
        ui.label("Error: " + str(e))
        return 1
    #ui.label("id del nuevomaterial: " + str(newMaterial))

    if new_form_notes.value:
        osapi.update_demos()
        osapi.selectDemoById(newMaterial).add_note(new_form_notes.value)

    if new_form_name.value:
        osapi.movFromTmp(tmpfiles, osapi.selectDemoById(newMaterial).path)
        osapi.emtpyTmp()

    #importante 
    ui.navigate.reload()



def view_item(item):
    print(item)
    demo = osapi.selectDemoById(item["ID"])
    print(demo.name)
    viewer_title.content = "#### **" + demo.name + "**"
    viewer_type.content =  "**" + item["type"] + "**"
    if os.path.isfile(demo.path + '/notes.txt'):  
        with open(demo.path + "/notes.txt", 'r') as file:
            viewer_about.content = file.read()
    else:
        viewer_about.content = ""

    # File listing
    files = osapi.listFiles(demo=demo, formats=["mp3", "wav", "ogg", "oga", "m4a", "aac", "flac"])
    print(files)

    
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

        with ui.expansion('Viewer', icon='visibility', group='left', value = True).classes('w-full'):
            viewer_title = ui.markdown('#### **' + osapi.demos[-1].name + '**')
            viewer_type = ui.markdown('**' + types[osapi.demos[-1].type] + '**')
            ui.label('About: ')
            viewer_about = ui.markdown("...")
            if os.path.isfile(osapi.demos[-1].path + '/notes.txt'):  
                with open(osapi.demos[-1].path + "/notes.txt", 'r') as file:
                    viewer_about.content = file.read()
                    
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
            uitable.on('view', lambda val: view_item(val.args['row']))
            
        #table.on('action', lambda msg: print(msg))

ui.run(port=8081, reload=False)
    
