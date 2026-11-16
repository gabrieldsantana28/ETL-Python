from datetime import datetime

ano = datetime.today().year
mes = datetime.today().month

COMPETENCIAATUAL = int(f"{ano}{mes:02d}")

# Parâmetros para extração dos dados da RNP
UNIMEDEXECDE = 611
UNIMEDEXECATE = 635
TIPOPREST = 0
PAGGERADO = 'S'



