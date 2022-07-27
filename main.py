import web2citwrapper

page = web2citwrapper.Page(
    'https://www.elpais.com.uy/informacion/politica/lacalle-salio-cruce-diputado-mpp-dijo-hay-ola-robos-violentos.html')

print(page.score())

domain = web2citwrapper.Domain('www.elobservador.com.uy')

print(domain.score())
