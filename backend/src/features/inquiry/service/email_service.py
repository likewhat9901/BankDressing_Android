import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import logging
from src.core.config.email_config import (
    SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, INQUIRY_RECIPIENT
)
from src.features.inquiry.util.email_template import format_inquiry_email_body

logger = logging.getLogger(__name__)


def send_inquiry_email(subject: str, body: str, sender_email: str | None = None) -> bool:
    """문의 이메일 발송"""
    
    if not all([SMTP_USER, SMTP_PASSWORD, INQUIRY_RECIPIENT]):
        logger.error("이메일 설정이 완료되지 않았습니다")
        raise ValueError("이메일 설정이 완료되지 않았습니다")
    
    try:
        # 이메일 메시지 생성
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = INQUIRY_RECIPIENT
        msg['Subject'] = f"[뱅크드레싱 문의] {subject}"
        
        # 본문 구성
        email_body = format_inquiry_email_body(subject, body, sender_email)
        msg.attach(MIMEText(email_body, 'plain', 'utf-8'))
        
        # SMTP 연결 및 발송
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        
        logger.info(f"문의 이메일 발송 완료: {subject}")
        return True
        
    except Exception as e:
        logger.error(f"이메일 발송 실패: {e}")
        raise