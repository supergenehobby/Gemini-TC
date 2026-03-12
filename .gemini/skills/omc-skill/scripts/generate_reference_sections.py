#!/usr/bin/env python3
"""
Generate Reference Section Files from PDF with Understanding Evaluation

PDF를 파싱하고 이해도를 평가한 후 섹션별 MD 파일을 자동 생성하는 스크립트
이해도가 75점 미만이면 자동으로 질문하여 명확히 한 후 MD 파일을 생성합니다.

Usage:
    python generate_reference_sections.py solitaire
    python generate_reference_sections.py [game_name]
"""

import os
import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import json

try:
    import PyPDF2
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False
    print("⚠️  Warning: PyPDF2 not installed. Install with: pip install PyPDF2")

# ============================================================================
# Configuration
# ============================================================================

BASE_DIR = Path(__file__).parent.parent
REFERENCE_DIR = BASE_DIR / ".omc" / "reference"
GEMINI_REFERENCE_DIR = BASE_DIR / ".gemini" / "reference"

# 이해도 기준점
UNDERSTANDING_THRESHOLD = 75  # 75점 이상이어야 함

# ============================================================================
# Helper Functions
# ============================================================================

def find_index_file(game_name: str) -> Path:
    """
    게임명 기반으로 인덱스 파일 찾기
    
    예: solitaire → [PST] Solitaire Tripeaks (2)-index.md
    """
    game_folder = REFERENCE_DIR / f"[{game_name.capitalize()}]"
    
    if not game_folder.exists():
        print(f"❌ 폴더를 찾을 수 없습니다: {game_folder}")
        sys.exit(1)
    
    index_files = list(game_folder.glob("*-index.md"))
    
    if not index_files:
        print(f"❌ 인덱스 파일을 찾을 수 없습니다: {game_folder}")
        sys.exit(1)
    
    return index_files[0]

def find_pdf_file(game_name: str) -> Optional[Path]:
    """
    게임명 기반으로 PDF 파일 찾기
    
    예: solitaire → [PST] Solitaire Tripeaks (2).pdf
    """
    if not GEMINI_REFERENCE_DIR.exists():
        print(f"⚠️  PDF 폴더를 찾을 수 없습니다: {GEMINI_REFERENCE_DIR}")
        return None
    
    # 게임명으로 PDF 찾기 (대소문자 무시)
    game_lower = game_name.lower()
    pdf_files = [f for f in GEMINI_REFERENCE_DIR.glob("*.pdf") 
                 if game_lower in f.name.lower()]
    
    if not pdf_files:
        print(f"⚠️  PDF 파일을 찾을 수 없습니다: {GEMINI_REFERENCE_DIR}")
        return None
    
    return pdf_files[0]

def parse_index_table(index_path: Path) -> List[Dict]:
    """
    인덱스 파일을 파싱하여 섹션 정보 추출
    
    마크다운 테이블 형식:
    | # | Section | Pages | Summary |
    |---|---------|-------|---------|
    | 01 | 개요 | 4–20 | ... |
    """
    sections = []
    
    with open(index_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    in_table = False
    for line in lines:
        if '| # | Section' in line:
            in_table = True
            continue
        
        if line.strip().startswith('|') and '---' in line:
            continue
        
        if in_table and line.strip().startswith('|'):
            if '|' not in line or line.strip() == '':
                break
            
            parts = [p.strip() for p in line.split('|')]
            
            if len(parts) >= 5 and parts[1] and parts[2]:
                try:
                    no = parts[1]
                    section_name = parts[2]
                    pages = parts[3]
                    summary = parts[4] if len(parts) > 4 else ""
                    
                    if no[0].isdigit():
                        sections.append({
                            'no': no,
                            'name': section_name,
                            'pages': pages,
                            'summary': summary
                        })
                except (IndexError, ValueError):
                    continue
    
    return sections

def parse_page_range(pages_str: str) -> Tuple[int, int]:
    """
    페이지 범위 문자열 파싱
    
    예: "4–20" → (4, 20)
    """
    try:
        parts = pages_str.replace('–', '-').replace('—', '-').split('-')
        start = int(parts[0].strip())
        end = int(parts[1].strip()) if len(parts) > 1 else start
        return start, end
    except (ValueError, IndexError):
        return 1, 1

def extract_pdf_text(pdf_path: Path, start_page: int, end_page: int) -> str:
    """
    PDF에서 특정 페이지 범위의 텍스트 추출
    """
    if not HAS_PYPDF:
        return "[PDF 파싱 불가능]\n\n전체 내용을 수동으로 입력해주세요."
    
    try:
        text = ""
        with open(pdf_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            total_pages = len(pdf_reader.pages)
            
            # 페이지 범위 조정 (0-based indexing)
            start_idx = max(0, start_page - 1)
            end_idx = min(total_pages, end_page)
            
            for page_idx in range(start_idx, end_idx):
                page = pdf_reader.pages[page_idx]
                text += f"\n--- Page {page_idx + 1} ---\n"
                text += page.extract_text()
        
        return text
    except Exception as e:
        print(f"⚠️  PDF 추출 오류: {e}")
        return f"[PDF 추출 오류]\n\n전체 내용을 수동으로 입력해주세요."

def evaluate_understanding(content: str) -> int:
    """
    이해도 평가 (0-100점)
    
    평가 항목:
    - Feature 식별 여부
    - 시스템 규칙 명확성
    - 데이터 흐름 정의
    - Edge case 식별
    - 모호함 제거
    """
    score = 0
    
    # Feature 식별 (20점)
    if re.search(r'(feature|functionality|capability|behavior)', content, re.I):
        score += 10
    if len(content.split('\n')) > 5:  # 최소 텍스트량
        score += 10
    
    # 시스템 규칙 명확성 (20점)
    if re.search(r'(rule|condition|requirement|constraint|when|if)', content, re.I):
        score += 10
    if re.search(r'(\d+|percentage|amount|value)', content):  # 구체적 수치
        score += 10
    
    # 데이터 흐름 정의 (20점)
    if re.search(r'(input|output|data|flow|process|state)', content, re.I):
        score += 10
    if re.search(r'(change|update|modify|transition)', content, re.I):
        score += 10
    
    # Edge case 식별 (20점)
    if re.search(r'(error|exception|fail|invalid|edge|boundary)', content, re.I):
        score += 10
    if re.search(r'(when|if|scenario|case|situation)', content, re.I):
        score += 10
    
    # 모호함 제거 (20점)
    if not re.search(r'(TBD|TODO|TK|TBA|unclear|unknown|maybe)', content, re.I):
        score += 10
    if len([line for line in content.split('\n') if line.strip()]) > 10:
        score += 10
    
    return min(100, score)

def identify_unclear_areas(content: str, score: int) -> List[str]:
    """
    명확하지 않은 부분 식별
    """
    unclear_areas = []
    
    if score < 50:
        unclear_areas.append("전체 내용의 구조와 흐름")
    
    if not re.search(r'(feature|functionality|capability)', content, re.I):
        unclear_areas.append("주요 기능 및 특징")
    
    if not re.search(r'(rule|condition|requirement)', content, re.I):
        unclear_areas.append("시스템 규칙 및 제약 조건")
    
    if not re.search(r'(error|exception|fail)', content, re.I):
        unclear_areas.append("예외 처리 및 에러 시나리오")
    
    if not re.search(r'(\d+|percentage|amount)', content):
        unclear_areas.append("구체적인 수치 및 배율")
    
    return unclear_areas

def get_clarification_from_user(section_name: str, unclear_areas: List[str], score: int) -> str:
    """
    사용자로부터 명확화 입력 받기
    """
    print(f"\n⚠️  [{section_name}] 섹션의 이해도가 {score}점입니다.")
    print(f"다음 부분이 명확하지 않습니다:\n")
    
    for i, area in enumerate(unclear_areas, 1):
        print(f"  {i}. {area}")
    
    print(f"\n다음 정보를 입력해주세요 (각 항목은 줄바꿈으로 분리):")
    print("=" * 60)
    
    clarifications = []
    for area in unclear_areas:
        print(f"\n[{area}]")
        user_input = input("→ ").strip()
        if user_input:
            clarifications.append(f"**{area}**\n{user_input}")
    
    print("\n" + "=" * 60)
    return "\n\n".join(clarifications)

def merge_clarification(pdf_content: str, clarification: str) -> str:
    """
    PDF 내용과 사용자 명확화 병합
    """
    merged = f"{pdf_content}\n\n## 명확화된 내용\n\n{clarification}"
    return merged

def generate_section_md(section_name: str, section_info: Dict, content: str) -> str:
    """
    섹션별 MD 파일 내용 생성
    
    실제 PDF 내용을 기반으로 생성
    """
    # 내용에서 주요 정보 추출
    features_section = extract_features(content)
    rules_section = extract_rules(content)
    flow_section = extract_data_flow(content)
    exceptions_section = extract_exceptions(content)
    
    template = f"""# {section_name} (Pages {section_info['pages']})

## Overview
{section_info['summary']}

### Key Components
{extract_key_components(content)}

---

## Features

{features_section if features_section else '''### Feature 1: [Feature Name]
- **Description**: 기능 설명
- **Specifications**: 상세 스펙
- **UI/UX Details**: UI/UX 상세사항
- **Edge Cases**: 엣지 케이스

### Feature 2: [Feature Name]
- **Description**: 기능 설명
- **Specifications**: 상세 스펙
- **UI/UX Details**: UI/UX 상세사항
- **Edge Cases**: 엣지 케이스'''}

---

## System Rules

{rules_section if rules_section else '''- **Rule 1**: 시스템 규칙 1
- **Rule 2**: 시스템 규칙 2
- **Rule 3**: 시스템 규칙 3'''}

---

## Data Flow

### Input/Output Specifications
- **Input**: 입력 데이터 형식
- **Output**: 출력 데이터 형식

### State Transitions
{flow_section if flow_section else '''- **State 1 → State 2**: 전이 조건
- **State 2 → State 3**: 전이 조건'''}

### Data Consistency Rules
- **Rule 1**: 데이터 일관성 규칙
- **Rule 2**: 데이터 일관성 규칙

---

## Exception Handling

### Error Scenarios
{exceptions_section if exceptions_section else '''1. **Error 1**: 에러 시나리오 1
   - **Recovery**: 복구 방법
   - **Message**: 사용자 메시지

2. **Error 2**: 에러 시나리오 2
   - **Recovery**: 복구 방법
   - **Message**: 사용자 메시지

3. **Error 3**: 에러 시나리오 3
   - **Recovery**: 복구 방법
   - **Message**: 사용자 메시지'''}

---

## 원본 내용

```
{content[:1000]}...
```

---

**Generated by**: generate_reference_sections.py (v2 with Understanding Evaluation)
**Source**: Pages {section_info['pages']}
**Understanding Score**: {evaluate_understanding(content)}점
"""
    return template

def extract_key_components(content: str) -> str:
    """내용에서 주요 컴포넌트 추출"""
    lines = [line.strip() for line in content.split('\n') if line.strip() and len(line.strip()) > 20]
    if lines:
        return "\n".join([f"- {line}" for line in lines[:3]])
    return "- [주요 컴포넌트 자동 추출 불가]"

def extract_features(content: str) -> str:
    """내용에서 Feature 추출"""
    if re.search(r'(feature|functionality|capability)', content, re.I):
        matches = re.findall(r'(?:feature|functionality)[:\s]+([^\n]+)', content, re.I)
        if matches:
            return "\n".join([f"### {match}\n- 설명 추가" for match in matches[:3]])
    return ""

def extract_rules(content: str) -> str:
    """내용에서 System Rules 추출"""
    if re.search(r'(rule|condition|requirement)', content, re.I):
        matches = re.findall(r'(?:rule|condition)[:\s]+([^\n]+)', content, re.I)
        if matches:
            return "\n".join([f"- **{match}**" for match in matches[:3]])
    return ""

def extract_data_flow(content: str) -> str:
    """내용에서 Data Flow 추출"""
    if re.search(r'(transition|change|state)', content, re.I):
        matches = re.findall(r'(?:transition|state)[:\s]+([^\n]+)', content, re.I)
        if matches:
            return "\n".join([f"- {match}" for match in matches[:3]])
    return ""

def extract_exceptions(content: str) -> str:
    """내용에서 Exception 추출"""
    if re.search(r'(error|exception|fail)', content, re.I):
        matches = re.findall(r'(?:error|exception)[:\s]+([^\n]+)', content, re.I)
        if matches:
            return "\n".join([f"{i+1}. **{match}**\n   - 복구 방법\n   - 사용자 메시지" 
                            for i, match in enumerate(matches[:3])])
    return ""

def create_reference_files(game_name: str):
    """
    메인 함수: PDF 파싱 → 이해도 평가 → MD 파일 생성
    """
    print(f"\n🚀 Reference 섹션 파일 생성 시작: {game_name}")
    print("=" * 70)
    
    # Step 1: 인덱스 파일 찾기
    print(f"\n📋 Step 1: 인덱스 파일 찾기...")
    index_path = find_index_file(game_name)
    print(f"✅ 인덱스 파일 발견: {index_path.name}")
    
    # Step 2: 인덱스 파싱
    print(f"\n📊 Step 2: 인덱스 파싱...")
    sections = parse_index_table(index_path)
    print(f"✅ {len(sections)}개 섹션 발견:")
    for section in sections:
        print(f"   [{section['no']}] {section['name']} (Pages {section['pages']})")
    
    # Step 3: PDF 파일 찾기
    print(f"\n📄 Step 3: PDF 파일 찾기...")
    pdf_path = find_pdf_file(game_name)
    if pdf_path:
        print(f"✅ PDF 파일 발견: {pdf_path.name}")
    else:
        print(f"⚠️  PDF 파일 없음 - 수동 입력 모드")
    
    # Step 4: 출력 디렉토리 준비
    print(f"\n📁 Step 4: 출력 디렉토리 준비...")
    output_dir = index_path.parent
    print(f"✅ 출력 디렉토리: {output_dir}")
    
    # Step 5: 섹션별 MD 파일 생성 (이해도 평가 포함)
    print(f"\n✍️  Step 5: 섹션별 MD 파일 생성 (이해도 평가 포함)...")
    created_files = []
    
    for section in sections:
        print(f"\n   📌 [{section['no']}] {section['name']} 처리 중...")
        
        # 5-1: PDF에서 텍스트 추출
        if pdf_path:
            start_page, end_page = parse_page_range(section['pages'])
            pdf_content = extract_pdf_text(pdf_path, start_page, end_page)
        else:
            pdf_content = "[PDF 없음] 내용을 수동으로 입력해주세요."
        
        # 5-2: 이해도 평가
        understanding_score = evaluate_understanding(pdf_content)
        print(f"      🎯 이해도 평가: {understanding_score}점", end="")
        
        # 5-3: 이해도 부족 시 명확화
        if understanding_score < UNDERSTANDING_THRESHOLD:
            print(f" (기준: {UNDERSTANDING_THRESHOLD}점) ⚠️")
            
            unclear_areas = identify_unclear_areas(pdf_content, understanding_score)
            clarification = get_clarification_from_user(section['name'], unclear_areas, understanding_score)
            pdf_content = merge_clarification(pdf_content, clarification)
            
            # 재평가
            understanding_score = evaluate_understanding(pdf_content)
            print(f"      🔄 재평가: {understanding_score}점", end="")
        
        print(f" ✅" if understanding_score >= UNDERSTANDING_THRESHOLD else f" ⚠️")
        
        # 5-4: MD 파일 생성
        section_slug = section['name'].replace(' ', '_').lower()
        filename = f"{section['no']}_{section_slug}.md"
        filepath = output_dir / filename
        
        content = generate_section_md(section['name'], section, pdf_content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        created_files.append(filename)
        print(f"      💾 파일 저장: {filename}")
    
    # Step 6: 완료
    print(f"\n" + "=" * 70)
    print(f"🎉 완료!")
    print(f"✅ {len(created_files)}개 파일 생성됨")
    print(f"📂 위치: {output_dir}")
    print(f"\n다음 단계:")
    print(f"   > omc: generate-tc {game_name}")
    print(f"\n" + "=" * 70 + "\n")

# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_reference_sections.py [game_name]")
        print("Example: python generate_reference_sections.py solitaire")
        sys.exit(1)
    
    game_name = sys.argv[1]
    create_reference_files(game_name)
