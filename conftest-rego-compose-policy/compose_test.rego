package main

# conftest verify 가 읽는 단위 시험이다. 규칙마다 걸려야 하는 입력과 걸리면 안 되는 입력을 한 쌍씩 둔다.

base := {"image": "app:1.0", "user": "1000", "read_only": true}

has(msgs, word) if {
	some m in msgs
	contains(m, word)
}

test_privileged_denied if {
	has(deny, "privileged") with input as {"services": {"a": object.union(base, {"privileged": true})}}
}

test_privileged_absent_ok if {
	not has(deny, "privileged") with input as {"services": {"a": base}}
}

test_host_network_denied if {
	has(deny, "network_mode host") with input as {"services": {"a": object.union(base, {"network_mode": "host"})}}
}

test_docker_sock_denied if {
	has(deny, "docker.sock") with input as {"services": {"a": object.union(base, {"volumes": ["/var/run/docker.sock:/var/run/docker.sock"]})}}
}

test_normal_volume_ok if {
	not has(deny, "docker.sock") with input as {"services": {"a": object.union(base, {"volumes": ["data:/var/lib/data"]})}}
}

test_latest_tag_denied if {
	has(deny, "태그를 고정") with input as {"services": {"a": object.union(base, {"image": "nginx:latest"})}}
}

test_no_tag_denied if {
	has(deny, "태그를 고정") with input as {"services": {"a": object.union(base, {"image": "nginx"})}}
}

test_pinned_tag_ok if {
	not has(deny, "태그를 고정") with input as {"services": {"a": base}}
}

test_digest_ok if {
	not has(deny, "태그를 고정") with input as {"services": {"a": object.union(base, {"image": "nginx@sha256:abc"})}}
}

test_literal_password_denied if {
	has(deny, "비밀값") with input as {"services": {"a": object.union(base, {"environment": {"DB_PASSWORD": "hunter2"}})}}
}

test_password_from_variable_ok if {
	not has(deny, "비밀값") with input as {"services": {"a": object.union(base, {"environment": {"DB_PASSWORD": "${DB_PASSWORD}"}})}}
}

test_root_user_warned if {
	has(warn, "user 를 지정") with input as {"services": {"a": {"image": "app:1.0"}}}
}

test_open_port_warned if {
	has(warn, "모든 인터페이스") with input as {"services": {"a": object.union(base, {"ports": ["8080:80"]})}}
}

test_loopback_port_ok if {
	not has(warn, "모든 인터페이스") with input as {"services": {"a": object.union(base, {"ports": ["127.0.0.1:8080:80"]})}}
}
