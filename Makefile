IMAGE_NAME=discussremover
DOCKER_REGISTRY=cr.yandex/crp50vbrjt40fspljvo7

update:
	@echo '<<<Builing Docker image..>>>'
	docker build -t $(IMAGE_NAME) .
	docker tag $(IMAGE_NAME):latest $(DOCKER_REGISTRY)/$(IMAGE_NAME):$(version)
	docker push $(DOCKER_REGISTRY)/$(IMAGE_NAME):$(version)

