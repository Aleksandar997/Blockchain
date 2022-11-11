import daemon
from crypto_dns_seed import main
class CustomDaemon(daemon):
    def run(self):
        init = main()
        init.run()