api-path = app/api/api_v1

clean:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

run:
	uvicorn app.main:app --reload

# On Terminal type: make module module_name
module:
	 @mkdir $(api-path)/$(filter-out $@,$(MAKECMDGOALS))
	 @echo "Creating directory $(api-path)/$(filter-out $@,$(MAKECMDGOALS)) ... done"
	 @touch $(api-path)/$(filter-out $@,$(MAKECMDGOALS))/__init__.py
	 @echo "Generating $(api-path)/$(filter-out $@,$(MAKECMDGOALS))/__init__.py ... done"
	 @touch $(api-path)/$(filter-out $@,$(MAKECMDGOALS))/repository.py
	 @echo "Generating $(api-path)/$(filter-out $@,$(MAKECMDGOALS))/repository.py ... done"
	 @touch $(api-path)/$(filter-out $@,$(MAKECMDGOALS))/service.py
	 @echo "Generating $(api-path)/$(filter-out $@,$(MAKECMDGOALS))/service.py ... done"
	 @touch $(api-path)/$(filter-out $@,$(MAKECMDGOALS))/endpoints.py
	 @echo "Generating $(api-path)/$(filter-out $@,$(MAKECMDGOALS))/endpoints.py ... done" 

%:
	@:

git-log:
	git log --oneline --graph --color --all --decorate

config-git-log:
	git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"

lint:
	bash scripts/lint.sh

format:
	bash scripts/format.sh

format-import:
	bash scripts/format-imports.sh