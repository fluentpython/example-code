import ObjetoSecreto

oSecreto = ObjetoSecreto('senha super secreta')
campoPrivado = ObjetoSecreto.getDeclaredField('escondido')
campoPrivado.setAccessible(True) # arrombamos a porta
print 'oSecreto.escondido =', campoPrivado.get(oSecreto)
