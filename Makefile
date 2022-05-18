.PHONY: install
install:
	pip3 install -r requirements.txt
	cp mastodon_bot.service /etc/systemd/system/monero_bot.service
	systemctl daemon-reload

.PHONY: restart
restart:
	systemctl stop monero_bot.service
	systemctl start monero_bot.service

.PHONY: status
status:
	systemctl status monero_bot.service

.PHONY: stop
stop:
	systemctl stop monero_bot.service

.PHONY: start
start:
	systemctl start monero_bot.service
