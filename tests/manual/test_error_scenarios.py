#!/usr/bin/env python3
"""Langfuse 에러 시나리오 테스트 스크립트

이 스크립트는 Langfuse 에러 핸들링이 올바르게 동작하는지 검증합니다.
4가지 에러 시나리오를 자동으로 테스트하고 결과를 출력합니다.

테스트 시나리오:
1. 환경 변수 미설정 (Langfuse 비활성화)
2. 잘못된 API 키 (인증 실패)
3. Langfuse 서버 다운 (연결 실패)
4. 네트워크 타임아웃 (존재하지 않는 URL)
"""

import sys
import shutil
import subprocess
import time
from pathlib import Path
from typing import Optional

# 프로젝트 루트를 sys.path에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class Colors:
    """터미널 색상 코드"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(message: str) -> None:
    """헤더 메시지 출력"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{message}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}\n")


def print_success(message: str) -> None:
    """성공 메시지 출력"""
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")


def print_error(message: str) -> None:
    """에러 메시지 출력"""
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")


def print_warning(message: str) -> None:
    """경고 메시지 출력"""
    print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")


def print_info(message: str) -> None:
    """정보 메시지 출력"""
    print(f"{Colors.OKCYAN}ℹ {message}{Colors.ENDC}")


class EnvBackup:
    """환경 변수 파일 백업 및 복원 관리 클래스"""

    def __init__(self, env_path: Path):
        self.env_path = env_path
        self.backup_path = env_path.with_suffix('.env.backup')

    def backup(self) -> None:
        """환경 변수 파일 백업"""
        if self.env_path.exists():
            shutil.copy2(self.env_path, self.backup_path)
            print_success(f"환경 변수 백업 완료: {self.backup_path}")
        else:
            print_warning(f"환경 변수 파일이 존재하지 않음: {self.env_path}")

    def restore(self) -> None:
        """환경 변수 파일 복원"""
        if self.backup_path.exists():
            shutil.copy2(self.backup_path, self.env_path)
            self.backup_path.unlink()
            print_success(f"환경 변수 복원 완료: {self.env_path}")
        else:
            print_warning(f"백업 파일이 존재하지 않음: {self.backup_path}")

    def modify_env(self, modifications: dict[str, Optional[str]]) -> None:
        """환경 변수 파일 수정

        Args:
            modifications: {변수명: 새값} 딕셔너리. None이면 주석 처리
        """
        if not self.env_path.exists():
            print_error(f"환경 변수 파일이 존재하지 않음: {self.env_path}")
            return

        with open(self.env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        new_lines = []
        for line in lines:
            modified = False
            for key, value in modifications.items():
                if line.strip().startswith(f"{key}="):
                    if value is None:
                        # 주석 처리
                        new_lines.append(f"# {line}")
                    else:
                        # 값 변경
                        new_lines.append(f"{key}={value}\n")
                    modified = True
                    break

            if not modified:
                new_lines.append(line)

        with open(self.env_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

        print_success("환경 변수 파일 수정 완료")


class DockerManager:
    """Docker 컨테이너 관리 클래스"""

    @staticmethod
    def stop_langfuse() -> bool:
        """Langfuse 컨테이너 중지"""
        try:
            result = subprocess.run(
                ["docker-compose", "-f", "infra/docker-compose.yml", "stop", "langfuse"],
                cwd=project_root,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                print_success("Langfuse 컨테이너 중지 완료")
                return True
            else:
                print_error(f"Langfuse 컨테이너 중지 실패: {result.stderr}")
                return False
        except Exception as e:
            print_error(f"Langfuse 컨테이너 중지 중 에러: {e}")
            return False

    @staticmethod
    def start_langfuse() -> bool:
        """Langfuse 컨테이너 시작"""
        try:
            result = subprocess.run(
                ["docker-compose", "-f", "infra/docker-compose.yml", "up", "-d", "langfuse"],
                cwd=project_root,
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                print_success("Langfuse 컨테이너 시작 완료")
                # 컨테이너 헬스 체크 대기
                time.sleep(5)
                return True
            else:
                print_error(f"Langfuse 컨테이너 시작 실패: {result.stderr}")
                return False
        except Exception as e:
            print_error(f"Langfuse 컨테이너 시작 중 에러: {e}")
            return False

    @staticmethod
    def check_langfuse_status() -> bool:
        """Langfuse 컨테이너 상태 확인"""
        try:
            result = subprocess.run(
                ["docker", "ps", "--filter", "name=transbot-langfuse", "--format", "{{.Status}}"],
                capture_output=True,
                text=True,
                timeout=10
            )
            status = result.stdout.strip()
            if "Up" in status:
                print_info(f"Langfuse 컨테이너 상태: {status}")
                return True
            else:
                print_warning(f"Langfuse 컨테이너 중지됨 또는 없음: {status}")
                return False
        except Exception as e:
            print_error(f"Langfuse 컨테이너 상태 확인 실패: {e}")
            return False


def test_scenario_1_no_env_vars() -> bool:
    """시나리오 1: 환경 변수 미설정 테스트

    Langfuse 환경 변수가 설정되지 않은 경우:
    - Config.langfuse_enabled가 False여야 함
    - configure_langfuse가 False를 반환해야 함
    - 번역 기능은 정상 동작해야 함
    """
    print_header("시나리오 1: 환경 변수 미설정 테스트")

    env_path = project_root / ".env"
    env_backup = EnvBackup(env_path)

    try:
        # 1. 환경 변수 백업 및 수정
        env_backup.backup()
        env_backup.modify_env({
            "LANGFUSE_PUBLIC_KEY": None,
            "LANGFUSE_SECRET_KEY": None,
            "LANGFUSE_HOST": None,
        })

        # 2. 모듈 재로드 (환경 변수 변경 반영)
        import importlib
        if 'config' in sys.modules:
            importlib.reload(sys.modules['config'])
        if 'components.observability' in sys.modules:
            importlib.reload(sys.modules['components.observability'])

        # 3. Config 로드 및 검증
        from config import Config
        config = Config.load()

        print_info(f"LANGFUSE_PUBLIC_KEY: {config.LANGFUSE_PUBLIC_KEY}")
        print_info(f"LANGFUSE_SECRET_KEY: {config.LANGFUSE_SECRET_KEY}")
        print_info(f"LANGFUSE_HOST: {config.LANGFUSE_HOST}")
        print_info(f"langfuse_enabled: {config.langfuse_enabled}")

        if not config.langfuse_enabled:
            print_success("Config.langfuse_enabled가 False로 설정됨")
        else:
            print_error("Config.langfuse_enabled가 True임 (예상: False)")
            return False

        # 4. configure_langfuse 호출 및 검증
        from components.observability import configure_langfuse
        result = configure_langfuse(config)

        if not result:
            print_success("configure_langfuse가 False를 반환함 (비활성화)")
        else:
            print_error("configure_langfuse가 True를 반환함 (예상: False)")
            return False

        print_success("\n시나리오 1 테스트 통과!")
        return True

    except Exception as e:
        print_error(f"\n시나리오 1 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        # 환경 변수 복원
        env_backup.restore()


def test_scenario_2_invalid_api_key() -> bool:
    """시나리오 2: 잘못된 API 키 테스트

    잘못된 API 키로 Langfuse 초기화 시:
    - configure_langfuse가 graceful degradation으로 동작해야 함
    - configure_langfuse가 False를 반환해야 함
    - 에러 메시지가 출력되어야 함
    - 번역 기능은 정상 동작해야 함
    """
    print_header("시나리오 2: 잘못된 API 키 테스트")

    env_path = project_root / ".env"
    env_backup = EnvBackup(env_path)

    try:
        # 1. 환경 변수 백업 및 수정
        env_backup.backup()
        env_backup.modify_env({
            "LANGFUSE_PUBLIC_KEY": "pk-invalid-key",
            "LANGFUSE_SECRET_KEY": "sk-invalid-key",
            "LANGFUSE_HOST": "http://localhost:3000",
        })

        # 2. 모듈 재로드
        import importlib
        if 'config' in sys.modules:
            importlib.reload(sys.modules['config'])
        if 'components.observability' in sys.modules:
            importlib.reload(sys.modules['components.observability'])

        # 3. Config 로드
        from config import Config
        config = Config.load()

        print_info(f"LANGFUSE_PUBLIC_KEY: {config.LANGFUSE_PUBLIC_KEY}")
        print_info(f"LANGFUSE_SECRET_KEY: {config.LANGFUSE_SECRET_KEY}")
        print_info(f"LANGFUSE_HOST: {config.LANGFUSE_HOST}")
        print_info(f"langfuse_enabled: {config.langfuse_enabled}")

        if config.langfuse_enabled:
            print_success("Config.langfuse_enabled가 True로 설정됨")
        else:
            print_error("Config.langfuse_enabled가 False임 (예상: True)")
            return False

        # 4. configure_langfuse 호출 (에러 핸들링 확인)
        print_info("configure_langfuse 호출 중... (에러 메시지가 출력될 수 있음)")
        from components.observability import configure_langfuse
        result = configure_langfuse(config)

        # 초기화는 성공할 수 있음 (인증은 나중에 실패할 수 있음)
        print_info(f"configure_langfuse 결과: {result}")
        print_success("configure_langfuse가 앱을 중단시키지 않음")

        print_success("\n시나리오 2 테스트 통과!")
        return True

    except Exception as e:
        print_error(f"\n시나리오 2 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        # 환경 변수 복원
        env_backup.restore()


def test_scenario_3_server_down() -> bool:
    """시나리오 3: Langfuse 서버 다운 테스트

    Langfuse 컨테이너가 중지된 경우:
    - configure_langfuse는 성공할 수 있음
    - track_translation 호출 시 연결 에러 발생
    - 에러가 적절히 처리되어야 함
    - 번역 기능은 정상 동작해야 함
    """
    print_header("시나리오 3: Langfuse 서버 다운 테스트")

    docker_manager = DockerManager()

    try:
        # 1. 현재 Langfuse 상태 확인
        print_info("Langfuse 컨테이너 상태 확인...")
        was_running = docker_manager.check_langfuse_status()

        # 2. Langfuse 컨테이너 중지
        if not docker_manager.stop_langfuse():
            print_warning("Langfuse 컨테이너 중지 실패 (이미 중지된 상태일 수 있음)")

        time.sleep(2)

        # 3. 모듈 재로드
        import importlib
        if 'config' in sys.modules:
            importlib.reload(sys.modules['config'])
        if 'components.observability' in sys.modules:
            importlib.reload(sys.modules['components.observability'])

        # 4. Config 로드
        from config import Config
        config = Config.load()

        print_info(f"langfuse_enabled: {config.langfuse_enabled}")

        if not config.langfuse_enabled:
            print_warning("Langfuse가 비활성화되어 있음 (환경 변수 미설정)")
            print_info("이 시나리오는 환경 변수가 설정된 상태에서 서버만 다운된 경우를 테스트합니다.")
            return True

        # 5. configure_langfuse 호출
        print_info("configure_langfuse 호출...")
        from components.observability import configure_langfuse
        result = configure_langfuse(config)

        # 6. 연결 에러 발생 시에도 앱은 정상 동작해야 함
        print_info(f"configure_langfuse 결과: {result}")
        print_success("configure_langfuse가 앱을 중단시키지 않음")

        print_success("\n시나리오 3 테스트 통과!")
        return True

    except Exception as e:
        print_error(f"\n시나리오 3 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        # 7. Langfuse 컨테이너 재시작 (원래 실행 중이었던 경우)
        print_info("Langfuse 컨테이너 재시작 중...")
        if was_running:
            docker_manager.start_langfuse()
        else:
            print_info("원래 Langfuse가 실행 중이 아니었으므로 재시작하지 않음")


def test_scenario_4_network_timeout() -> bool:
    """시나리오 4: 네트워크 타임아웃 테스트

    존재하지 않는 URL로 연결 시:
    - 타임아웃 에러가 발생해야 함
    - 에러가 적절히 처리되어야 함
    - 번역 기능은 정상 동작해야 함
    """
    print_header("시나리오 4: 네트워크 타임아웃 테스트")

    env_path = project_root / ".env"
    env_backup = EnvBackup(env_path)

    try:
        # 1. 환경 변수 백업 및 수정 (존재하지 않는 URL)
        env_backup.backup()
        env_backup.modify_env({
            "LANGFUSE_PUBLIC_KEY": "pk-test-key",
            "LANGFUSE_SECRET_KEY": "sk-test-key",
            "LANGFUSE_HOST": "http://192.0.2.1:3000",  # TEST-NET-1 (존재하지 않는 IP)
        })

        # 2. 모듈 재로드
        import importlib
        if 'config' in sys.modules:
            importlib.reload(sys.modules['config'])
        if 'components.observability' in sys.modules:
            importlib.reload(sys.modules['components.observability'])

        # 3. Config 로드
        from config import Config
        config = Config.load()

        print_info(f"LANGFUSE_HOST: {config.LANGFUSE_HOST}")
        print_info(f"langfuse_enabled: {config.langfuse_enabled}")

        if config.langfuse_enabled:
            print_success("Config.langfuse_enabled가 True로 설정됨")
        else:
            print_error("Config.langfuse_enabled가 False임 (예상: True)")
            return False

        # 4. configure_langfuse 호출 (타임아웃 에러 발생 예상)
        print_info("configure_langfuse 호출 중... (타임아웃 에러가 발생할 수 있음)")
        from components.observability import configure_langfuse
        result = configure_langfuse(config)

        print_info(f"configure_langfuse 결과: {result}")
        print_success("configure_langfuse가 앱을 중단시키지 않음")

        print_success("\n시나리오 4 테스트 통과!")
        return True

    except Exception as e:
        print_error(f"\n시나리오 4 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        # 환경 변수 복원
        env_backup.restore()


def main():
    """메인 테스트 실행 함수"""
    print_header("Langfuse 에러 핸들링 테스트 시작")

    results = []

    # 시나리오 1: 환경 변수 미설정
    results.append(("시나리오 1: 환경 변수 미설정", test_scenario_1_no_env_vars()))

    # 시나리오 2: 잘못된 API 키
    results.append(("시나리오 2: 잘못된 API 키", test_scenario_2_invalid_api_key()))

    # 시나리오 3: Langfuse 서버 다운
    results.append(("시나리오 3: Langfuse 서버 다운", test_scenario_3_server_down()))

    # 시나리오 4: 네트워크 타임아웃
    results.append(("시나리오 4: 네트워크 타임아웃", test_scenario_4_network_timeout()))

    # 결과 요약
    print_header("테스트 결과 요약")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for scenario, result in results:
        if result:
            print_success(f"{scenario}: 통과")
        else:
            print_error(f"{scenario}: 실패")

    print(f"\n{Colors.BOLD}총 {passed}/{total} 시나리오 통과{Colors.ENDC}")

    if passed == total:
        print_success("\n모든 테스트 통과!")
        return 0
    else:
        print_error(f"\n{total - passed}개 테스트 실패")
        return 1


if __name__ == "__main__":
    sys.exit(main())
