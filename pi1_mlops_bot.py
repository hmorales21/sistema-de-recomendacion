#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.
#le dejo los reconocimientos al autor de la librería
#importo mis librerías
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from surprise import Dataset
from surprise import Reader
from surprise import SVD
from surprise import accuracy
from surprise.model_selection import cross_validate
from surprise.model_selection import train_test_split
import joblib

import logging

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

contexto=''

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    global contexto
    user = update.effective_user
    await update.message.reply_html(
        rf"Hola {user.mention_html()}! Soy el bot del sistema de recomendación de películas de Horacio. Dime el número de usuario para hacerte una recomendación",
        reply_markup=ForceReply(selective=True),
    )
    contexto='espera usuario'

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Ayuda. La secuencia de comandos de ayuda se actualizará próximamente.")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """analiza el mensaje."""
    global contexto
    user = update.effective_user
    mensaje = update.message.text
    respuesta=''

    if contexto == 'espera usuario':
        userid=mensaje
        #busca las películas que el usuario ya ha visto
        #veamos cuales películas ha visto y que mejor ha calificado, vamos por 3 para arriba
        data_usuario = data_valoraciones[(data_valoraciones['rating']>=3.0) & (data_valoraciones['userId']==userid) ]
        #quitarlas de data_movies, nos deben quedar 22,998 - 1,511 =  21,487
        data_movies_seleccionado = data_movies[~data_movies['id'].isin(data_peliculas_fuera.id)]
        #quita las peliculas que ya vio el usuario
        data_movies_seleccionado = data_movies[~data_movies['id'].isin(data_usuario.movieId)]
        data_recomendaciones_posibles = data_movies_seleccionado[['id','title','score']]
        #hacemos la recomendación sobre el modelo previamente entrenado
        data_recomendaciones_posibles['ScoreEstimado'] = data_recomendaciones_posibles['id'].apply(lambda x: modelo.predict(userid, x).estcomojoblib)
        modelo.predict()
        respuesta ='aquí va la lista de películas que te recomiendo \n'
        contexto='pregunta volver a empezar'
    elif contexto =='pregunta volver a empezar':
        respuesta ='Espero haya alguna que te guste, ¿deseas continuar? \n'
        contexto='espera respuesta continuar'
    elif contexto=='espera respuesta continuar':
        if mensaje == 'si':
            respuesta =f'GRacias {user.first_name}! \n introduce otro número de usuario'
            contexto='espera usuario'
        else:
            respuesta =f'GRacias {user.first_name}! \n Espero haber sido útil'
            contexto=''
    elif contexto =='':
        respuesta = f"Hola {user.first_name}!\n Soy el bot del sistema de recomendación de películas de Horacio. Dime el número de usuario para hacerte una recomendación"
        contexto='espera usuario'

    await update.message.reply_text(respuesta)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6220351458:AAGzSt3f7-C1DyY6w0pa3uvMZftXniARss4").build()


    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    #application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    #primero carga el modelo entrenado
    modelo = joblib.load('./datasets_parciales/modelo_recomendaciones_entrenado.pkl') # Carga del modelo.
    #cargamos el dataset de películas
    data_movies=pd.read_csv('./datasets_parciales/titles_total.csv')
    data_valoraciones = pd.read_parquet('./datasets_parciales/valoraciones_para_modelo.parquet')
    data_no_consideradas=pd.read_csv('./datasets_parciales/moviesId_noconsideradas.csv')
    data_peliculas_fuera = pd.read_csv('./datasets_parciales/moviesId_noconsideradas.csv')
    contexto=''
    main()