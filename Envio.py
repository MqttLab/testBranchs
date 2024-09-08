class Envio():
    def __init__(self, cp, df, te, fp):
        self.codigo_postal = cp
        self.direccion_fisica = df
        self.tipo_envio = te
        self.forma_pago = fp

    def __str__(self):
        msg = f"Cod. Postal: {self.codigo_postal}\tDir.Fisica: {self.direccion_fisica}\tTipo Envio: {self.tipo_envio}\tForma Pago: {self.forma_pago}"
        return msg