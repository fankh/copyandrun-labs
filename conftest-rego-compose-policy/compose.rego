package main

# docker-compose.yml 한 파일을 입력으로 받아 deny(막음)와 warn(경고)을 만든다.

unpinned(image) if not contains(image, ":")

unpinned(image) if endswith(image, ":latest")

pinned_by_digest(image) if contains(image, "@sha256:")

secret_name(key) if regex.match(`(?i)(password|passwd|secret|token|api_?key)`, key)

deny contains msg if {
	some name, svc in input.services
	svc.privileged == true
	msg := sprintf("서비스 %s: privileged 를 쓰지 않습니다", [name])
}

deny contains msg if {
	some name, svc in input.services
	svc.network_mode == "host"
	msg := sprintf("서비스 %s: network_mode host 를 쓰지 않습니다", [name])
}

deny contains msg if {
	some name, svc in input.services
	some vol in svc.volumes
	is_string(vol)
	contains(vol, "docker.sock")
	msg := sprintf("서비스 %s: docker.sock 을 마운트하지 않습니다 (호스트 전체 권한과 같습니다)", [name])
}

deny contains msg if {
	some name, svc in input.services
	unpinned(svc.image)
	not pinned_by_digest(svc.image)
	msg := sprintf("서비스 %s: 이미지 %s 의 태그를 고정합니다 (latest 나 태그 없음 금지)", [name, svc.image])
}

deny contains msg if {
	some name, svc in input.services
	some key, value in svc.environment
	secret_name(key)
	is_string(value)
	not startswith(value, "${")
	msg := sprintf("서비스 %s: 환경 변수 %s 에 비밀값을 직접 적지 않습니다 (${변수}로 받습니다)", [name, key])
}

warn contains msg if {
	some name, svc in input.services
	not svc.user
	msg := sprintf("서비스 %s: user 를 지정해 root 로 실행하지 않습니다", [name])
}

warn contains msg if {
	some name, svc in input.services
	not svc.read_only
	msg := sprintf("서비스 %s: read_only: true 를 검토합니다", [name])
}

warn contains msg if {
	some name, svc in input.services
	some port in svc.ports
	not startswith(sprintf("%v", [port]), "127.0.0.1:")
	msg := sprintf("서비스 %s: 포트 %v 가 모든 인터페이스에 열립니다 (127.0.0.1: 로 제한을 검토합니다)", [name, port])
}
