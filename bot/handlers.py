from telegram import Update,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import  ContextTypes
from search import search_books

# Resultados por página
RESULTADOS_POR_PAGINA = 5

# Función para generar el mensaje paginado
def generar_mensaje_pagina(resultados, pagina):
    inicio = pagina * RESULTADOS_POR_PAGINA
    fin = inicio + RESULTADOS_POR_PAGINA
    subset = resultados[inicio:fin]

    texto = "📚 Resultados encontrados:\n\n"
    for i, libro in enumerate(subset, start=inicio + 1):
        texto += f"{i}. *{libro['Title']}*\n🔗 {libro['Link']}\n\n"
    return texto.strip()


# Función para generar los botones de paginado
def generar_botones(total, pagina):
    botones = []
    if pagina > 0:
        botones.append(InlineKeyboardButton("⬅️ Anterior", callback_data=f"pagina_{pagina - 1}"))
    if (pagina + 1) * RESULTADOS_POR_PAGINA < total:
        botones.append(InlineKeyboardButton("Siguiente ➡️", callback_data=f"pagina_{pagina + 1}"))
    return InlineKeyboardMarkup([botones]) if botones else None


# Manejo de mensajes comunes
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    resultados = search_books(texto)
    
    """
    # Verifica si la respuesta es una lista de diccionarios
    if isinstance(resultado,list) and resultado:
        mensaje = "📚 *Resultados encontrados:*\n\n"
        for i, libro in enumerate (resultado,start=1):
            titulo = libro.get("Title")
            link = libro.get("Link")
            year = libro.get("Public_Year")
            mensaje += f"{i}. *{titulo}*\n*Año publicacion:{year}*\n🔗{link}\n\n"
        await update.message.reply_text(mensaje,parse_mode="Markdown",disable_web_page_preview=True)
    else:
        await update.message.reply_text("❌ No se encontraron libros con ese título.")
    """
    if not resultados:
        await update.message.reply_text("❌ No se encontraron resultados.")
        return

    context.user_data["resultados"] = resultados  # Guardamos los resultados para este usuario
    mensaje = generar_mensaje_pagina(resultados, 0)
    botones = generar_botones(len(resultados), 0)

    await update.message.reply_text(
        mensaje,
        parse_mode="Markdown",
        reply_markup=botones,
        disable_web_page_preview=True
    )    

# Cuando se presiona un botón de paginación
async def manejar_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    datos = query.data
    if datos.startswith("pagina_"):
        pagina = int(datos.split("_")[1]) #Me quedo con la pagina en cuestion...
        resultados = context.user_data.get("resultados", [])
        mensaje = generar_mensaje_pagina(resultados, pagina)
        botones = generar_botones(len(resultados), pagina)

        await query.edit_message_text(
            text=mensaje,
            parse_mode="Markdown",
            reply_markup=botones,
            disable_web_page_preview=True
        )