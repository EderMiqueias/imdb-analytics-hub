from datetime import datetime


def diferenca_entre_datetimes(dt1: datetime, dt2: datetime):
    if dt1 > dt2:
        dt1, dt2 = dt2, dt1

    diferenca = dt2 - dt1

    segundos_totais = diferenca.seconds
    horas, resto = divmod(segundos_totais, 3600)
    minutos, segundos = divmod(resto, 60)
    print(f"- Minutos: {minutos}")
    print(f"- Segundos: {segundos}")
