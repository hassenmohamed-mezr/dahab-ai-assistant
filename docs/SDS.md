# AI WhatsApp Guest Assistant — Software Design Specification

Version: 1.1

## Table of Contents

- [1. Project Goal](#1-project-goal)
- [2. Project Overview](#2-project-overview)
- [3. Scope](#3-scope)
- [4. Functional Requirements](#4-functional-requirements)
  - [Guest Registration](#guest-registration)
  - [Welcome Message](#welcome-message)
  - [Chat](#chat)
  - [AI Assistant](#ai-assistant)
  - [Complaint](#complaint)
  - [Goodbye](#goodbye)
- [5. Non Functional Requirements](#5-non-functional-requirements)
- [6. User Roles](#6-user-roles)
  - [Guest](#guest)
  - [Owner](#owner)
- [7. Main Workflow](#7-main-workflow)
- [8. Tech Stack](#8-tech-stack)
- [9. System Components](#9-system-components)
- [10. Folder Structure](#10-folder-structure)
- [11. Folder Responsibilities](#11-folder-responsibilities)
- [12. Guest Lifecycle](#12-guest-lifecycle)
- [13. Database Design](#13-database-design)
  - [Guest](#guest-1)
  - [Conversation](#conversation)
  - [Message](#message)
  - [Notification](#notification)
  - [Settings](#settings)
- [14. Knowledge Source](#14-knowledge-source)
- [15. API Endpoints](#15-api-endpoints)
- [16. API Response Standard](#16-api-response-standard)
- [17. Message Processing Flow](#17-message-processing-flow)
- [18. AI Agent Architecture](#18-ai-agent-architecture)
- [19. Intent Mapping](#19-intent-mapping)
- [20. Tool Contracts](#20-tool-contracts)
- [21. Prompt Strategy](#21-prompt-strategy)
- [22. AI Prompt Rules](#22-ai-prompt-rules)
- [23. Error Handling](#23-error-handling)
- [24. Error Codes](#24-error-codes)
- [25. Environment Variables](#25-environment-variables)
- [26. Configuration Strategy](#26-configuration-strategy)
- [27. Coding Rules](#27-coding-rules)
- [28. Logging Strategy](#28-logging-strategy)
- [29. Scheduler Details](#29-scheduler-details)
- [30. Future Improvements](#30-future-improvements)
- [31. Development Plan](#31-development-plan)

---

## 1. Project Goal

يهدف المشروع إلى حل مشكلة التواصل المستمر بين صاحب الشقة السياحية والضيوف خلال فترة الإقامة. عادة ما يحتاج الضيف لمعلومات سريعة عن المكان المحيط، أو مساعدة في مشكلة بسيطة، أو التواصل مع المالك دون انتظار طويل، وهذا ما يستهلك وقت صاحب الشقة بشكل متكرر.

يوجد المساعد الذكي ليكون نقطة تواصل أولى تستجيب فوراً لمعظم الاستفسارات الشائعة (مطاعم، طقس، معلومات الشقة)، وتحول فقط الحالات التي تحتاج تدخل بشري فعلي إلى صاحب الشقة عبر Notification.

تجربة المستخدم المتوقعة: يتواصل الضيف عبر WhatsApp بشكل طبيعي كأنه يتحدث مع شخص، ويحصل على ردود سريعة ودقيقة، دون الحاجة لتحميل تطبيق إضافي أو المرور بعملية تسجيل معقدة.

الهدف الرئيسي للمشروع هو تقليل الحمل التشغيلي على صاحب الشقة، وتحسين تجربة الضيف، من خلال أتمتة الاستفسارات المتكررة والمهام الروتينية (الترحيب، الوداع، الأسئلة العامة).

من ناحية قابلية التوسع المستقبلي، تم تصميم البنية (Tools منفصلة، Services منفصلة عن API) بحيث يمكن مستقبلاً إضافة شقق جديدة أو أدوات إضافية دون تعقيد النظام الحالي، لكن هذا التوسع خارج نطاق الإصدار 1.0 ولا يجب البدء فيه الآن.

---

## 2. Project Overview

### الهدف

إنشاء مساعد ذكي يعمل عبر WhatsApp لمساعدة ضيوف الشقة السياحية طوال فترة إقامتهم.

النظام يجب أن:

- يستقبل الضيوف تلقائياً.
- يجيب عن أسئلتهم.
- يقدم معلومات محلية حقيقية.
- يساعد في حل المشكلات.
- ينبه صاحب الشقة عند الحاجة.
- يرسل رسائل تلقائية عند الوصول والمغادرة.

---

## 3. Scope

يشمل المشروع:

- Guest Registration
- Database
- WhatsApp Cloud API
- AI Agent
- Weather API
- Google Maps API
- Scheduler
- Owner Notifications

لا يشمل الإصدار الأول:

- Dashboard متقدم
- Payment System
- Booking Engine
- Multi Apartment
- Multi Owner

---

## 4. Functional Requirements

### Guest Registration

يقوم المسؤول بتسجيل:

- الاسم
- الهاتف
- الجنسية
- تاريخ الوصول
- تاريخ المغادرة

### Welcome Message

يرسل النظام رسالة ترحيب تلقائياً عند يوم الوصول.

### Chat

يمكن للضيف التحدث مع البوت عبر WhatsApp.

### AI Assistant

يدعم:

- المطاعم
- الكافيهات
- الأماكن السياحية
- الطقس
- معلومات الشقة
- الأسئلة العامة

### Complaint

عند وجود شكوى:

- إنشاء Notification
- إرسال تنبيه لصاحب الشقة

### Goodbye

عند المغادرة:

- رسالة وداع
- طلب تقييم

---

## 5. Non Functional Requirements

- زمن الرد أقل من 5 ثوانٍ.
- حفظ جميع الرسائل.
- سهولة إضافة Tools جديدة.
- تنظيم الكود.
- جميع المفاتيح داخل `.env`.

---

## 6. User Roles

### Guest

يمكنه:

- إرسال الرسائل
- استقبال الرسائل
- طلب المساعدة

### Owner

يمكنه:

- تسجيل الضيوف
- استقبال التنبيهات

---

## 7. Main Workflow

```text
Guest Registration

↓

Database

↓

Arrival Date

↓

Welcome Message

↓

Guest Chat

↓

AI Agent

↓

Choose Tool

↓

Generate Response

↓

WhatsApp

↓

Checkout

↓

Goodbye Message
```

---

## 8. Tech Stack

| Layer              | Technology          | Version              | Notes                        |
| ------------------- | -------------------- | ---------------------- | ----------------------------- |
| Language              | Python                  | 3.11+                     | Core language                     |
| Backend Framework     | FastAPI                 | Latest stable             | REST API layer                       |
| ORM                   | SQLAlchemy              | Latest stable             | Database abstraction                  |
| Database (Dev)        | SQLite                  | -                         | Local development                        |
| Database (Prod)       | PostgreSQL              | Latest stable             | Production database                       |
| Scheduler             | APScheduler             | Latest stable             | Background jobs                              |
| AI                    | OpenAI SDK              | Latest stable             | LLM integration                               |
| Messaging             | WhatsApp Cloud API      | Current Meta version      | Guest messaging                                |
| Maps                  | Google Maps API         | -                         | Places and directions                            |
| Weather               | OpenWeather API         | -                         | Weather information                               |
| Validation            | Pydantic                | v2                        | Request/response validation                        |
| Server                | Uvicorn                 | Latest stable             | ASGI server                                         |

ملاحظة: الإصدارات محددة بشكل عام (Latest stable) لأن المشروع صغير ولا يحتاج تثبيت نسخ صارمة الآن، ويمكن تحديدها في `requirements.txt` عند البدء الفعلي.

---

## 9. System Components

| Component            | Technology            |
| --------------------- | --------------------- |
| Backend                | FastAPI                |
| Database               | SQLite (Development)   |
| Production Database    | PostgreSQL              |
| AI                      | OpenAI GPT               |
| Messaging               | WhatsApp Cloud API        |
| Maps                    | Google Maps API            |
| Weather                 | OpenWeather API              |

---

## 10. Folder Structure

```text
project/

app.py
config.py
database.py
scheduler.py

api/
agent/
models/
services/
utils/
templates/
docs/
tests/

requirements.txt
```

**utils/** هو مجلد جديد يحتوي على دوال مساعدة مشتركة تُستخدم من أكثر من مكان في المشروع (Services، Agent، API)، ولا ترتبط بمنطق عمل محدد (business logic) حتى لا تتكرر داخل Services.

أمثلة على الملفات المتوقعة داخله:

- `logger.py`: إعداد وتنسيق الـ logging المستخدم في كل المشروع.
- `helpers.py`: دوال عامة صغيرة (تنسيق تاريخ، تنظيف نص، إلخ).
- `validators.py`: دوال تحقق مشتركة (مثل التحقق من صيغة رقم الهاتف).

القاعدة العامة: أي دالة مشتركة لا تحتوي على منطق عمل خاص بميزة معينة تذهب إلى `utils/` بدلاً من تكرارها داخل `services/`.

---

## 11. Folder Responsibilities

**api/**

مسؤول فقط عن HTTP endpoints.

بدون أي business logic.

**agent/**

مسؤول عن AI orchestration.

Intent detection.

Tool selection.

Prompt creation.

**services/**

Business logic.

External integrations (WhatsApp, Maps, Weather).

Database operations.

**models/**

Database entities (Guest, Conversation, Message, Notification, Settings).

**utils/**

Shared helper functions (logging setup, generic helpers, input validators).

لا يوجد بها business logic، فقط دوال مساعدة عامة يُعاد استخدامها في أكثر من مكان بدلاً من تكرارها داخل services/.

**templates/**

Static message templates (ترحيب، وداع، رسائل جاهزة).

**docs/**

Project documentation (SDS، ملاحظات إعداد، أي شرح إضافي للمشروع).

**tests/**

Unit and integration tests للـ Services والـ Tools والـ API.

**app.py**

نقطة تشغيل التطبيق وتجميع الـ routers.

**config.py**

تحميل الإعدادات والمفاتيح من `.env`.

**database.py**

إعداد الاتصال بقاعدة البيانات والـ session.

**scheduler.py**

تعريف وتشغيل الـ background jobs الدورية.

---

## 12. Guest Lifecycle

```text
Registered

↓

Waiting

↓

Checked-In

↓

Active

↓

Checkout

↓

Completed
```

**Registered**: تم تسجيل بيانات الضيف بواسطة المسؤول، ولم يصل تاريخ الوصول بعد.

**Waiting**: الضيف مسجل وبانتظار يوم الوصول، لا تفاعل بعد.

**Checked-In**: تاريخ الوصول قد حان، تم إرسال رسالة الترحيب.

**Active**: الضيف مقيم حالياً ويمكنه التفاعل مع البوت بشكل طبيعي.

**Checkout**: تاريخ المغادرة قد حان، يتم إرسال رسالة الوداع وطلب التقييم.

**Completed**: انتهت الإقامة، تُحفظ المحادثة كسجل ولا يتم إرسال رسائل جديدة تلقائياً.

---

## 13. Database Design

### Guest

| Field     | Type    |
| --------- | ------- |
| id        | Integer |
| name      | String  |
| phone     | String  |
| arrival   | Date    |
| departure | Date    |
| status    | String  |

### Conversation

| Field      | Type     |
| ---------- | -------- |
| id         | Integer  |
| guest_id   | Integer  |
| created_at | DateTime |

### Message

| Field           | Type     |
| --------------- | -------- |
| id              | Integer  |
| conversation_id | Integer  |
| role            | String   |
| content         | Text     |
| created_at      | DateTime |

### Notification

| Field    | Type    |
| -------- | ------- |
| id       | Integer |
| guest_id | Integer |
| message  | Text    |
| priority | String  |
| status   | String  |

### Settings

| Field | Type   |
| ----- | ------ |
| key   | String |
| value | Text   |

جدول `Settings` يخزن معلومات الشقة القابلة للتعديل بدلاً من كتابتها بشكل ثابت (hardcoded) داخل الكود، مثل:

- `wifi_password`
- `owner_phone`
- `checkin_time`
- `checkout_time`
- `parking_information`
- `house_rules`

بهذه الطريقة يمكن لصاحب الشقة تعديل هذه المعلومات دون الحاجة لتعديل الكود أو إعادة النشر.

---

## 14. Knowledge Source

بدلاً من الاعتماد على معلومات مكتوبة بشكل ثابت داخل الكود (hardcoded)، يعتمد الـ Knowledge Tool على ملف معرفة خارجي مثل:

```text
knowledge.json
```

أو

```text
knowledge.md
```

يقوم الـ AI بقراءة هذا الملف عند الحاجة للإجابة عن أسئلة تخص الشقة أو الأماكن السياحية المعروفة مسبقاً، بدلاً من الاعتماد على قيم مكتوبة داخل الكود.

هذا الأسلوب يسمح بتحديث معلومات الشقة بسهولة (إضافة أماكن جديدة، تعديل معلومة قديمة) دون الحاجة لتعديل أي كود أو إعادة نشر التطبيق.

الفرق بين `Settings` و `Knowledge Source`:

- **Settings**: قيم بسيطة (key/value) مثل كلمة سر الواي فاي أو رقم هاتف صاحب الشقة.
- **Knowledge Source**: معلومات أطول ووصفية (أماكن سياحية، تفاصيل عن الشقة، إجابات جاهزة) يقرأها الـ Knowledge Tool مباشرة.

---

## 15. API Endpoints

| Method | Endpoint         | Description                |
| ------ | ---------------- | --------------------------- |
| POST   | /register_guest  | Register Guest               |
| POST   | /webhook         | Receive WhatsApp Messages       |
| POST   | /send_message    | Send WhatsApp Message              |
| GET    | /guest/{id}      | Get Guest                             |
| GET    | /health          | Health Check                          |

`GET /health` يُستخدم لمراقبة حالة التطبيق أثناء النشر (deployment monitoring)، للتأكد من أن الخدمة تعمل وقادرة على الاستجابة قبل توجيه الترافيك إليها أو أثناء فحوصات الـ uptime الدورية.

---

## 16. API Response Standard

يجب أن تتبع جميع استجابات الـ API نفس الصيغة الموحدة:

```json
{
  "success": true,
  "message": "",
  "data": {},
  "error": null
}
```

شرح الحقول:

- **success**: قيمة Boolean توضح نجاح أو فشل العملية.
- **message**: نص وصفي مختصر يوضح نتيجة العملية للمستخدم أو للمطور.
- **data**: الكائن (Object) الذي يحتوي على البيانات الفعلية المُرجعة عند النجاح، ويكون فارغاً `{}` عند الفشل.
- **error**: يحتوي على تفاصيل الخطأ (مثل error code ووصفه) عند الفشل، ويكون `null` عند النجاح.

---

## 17. Message Processing Flow

```text
WhatsApp

↓

Webhook

↓

Validate Guest

↓

Load Context

↓

Intent Detection

↓

Select Tool

↓

Execute Tool

↓

Generate Prompt

↓

LLM

↓

Send Response

↓

Save Conversation
```

شرح كل خطوة:

- **WhatsApp**: مصدر الرسالة الواردة من الضيف.
- **Webhook**: نقطة الاستقبال في `/webhook` التي تستلم الـ payload من WhatsApp Cloud API.
- **Validate Guest**: التأكد أن رقم الهاتف مرتبط بضيف مسجل وحالته Active.
- **Load Context**: تحميل آخر المحادثة والبيانات ذات الصلة بالضيف من قاعدة البيانات.
- **Intent Detection**: تحديد نية الرسالة (مطعم، طقس، شكوى، سؤال عام...).
- **Select Tool**: اختيار الأداة المناسبة بناءً على الـ Intent المكتشف.
- **Execute Tool**: تنفيذ الأداة والحصول على نتيجة فعلية (بيانات حقيقية وليست مُختلقة).
- **Generate Prompt**: بناء الـ Prompt النهائي المرسل إلى الـ LLM باستخدام نتيجة الأداة والسياق.
- **LLM**: توليد الرد النهائي بلغة طبيعية باستخدام OpenAI.
- **Send Response**: إرسال الرد للضيف عبر WhatsApp Cloud API.
- **Save Conversation**: حفظ الرسالة والرد في جدول Message لأغراض السجل والسياق المستقبلي.

---

## 18. AI Agent Architecture

Workflow العام:

```text
Receive Message

↓

Validation

↓

Intent Detection

↓

Tool Selection

↓

Tool Execution

↓

Prompt Builder

↓

LLM

↓

Response
```

**Validation**: خطوة جديدة تُنفَّذ فور استقبال الرسالة، وتتأكد من أن الرسالة صالحة للمعالجة قبل الدخول في أي منطق ذكاء اصطناعي، مثل: التأكد من أن الضيف مسجل وحالته Active، وأن محتوى الرسالة ليس فارغاً أو بصيغة غير مدعومة. أي رسالة لا تجتاز هذه الخطوة تُرفض برد مناسب دون استهلاك استدعاء LLM.

### المكونات الداخلية

**Context Builder**

- Purpose: تجميع بيانات الضيف وآخر المحادثة لتكوين السياق.
- Input: guest_id، سجل المحادثة.
- Output: كائن Context جاهز للاستخدام.
- Responsibility: عدم تكرار استدعاء قاعدة البيانات أكثر من مرة لكل رسالة.

**Intent Detector**

- Purpose: تحديد نية الضيف من نص الرسالة.
- Input: نص الرسالة + Context.
- Output: اسم الـ Intent (مثال: Restaurant، Weather، Complaint).
- Responsibility: تصنيف دقيق وسريع دون استدعاء أدوات غير ضرورية.

**Tool Router**

- Purpose: اختيار الأداة المناسبة بناءً على الـ Intent.
- Input: اسم الـ Intent.
- Output: مرجع الأداة (Tool) المطلوب تنفيذها.
- Responsibility: التعامل مع الحالات التي لا يوجد فيها Tool مطابق (تحويل لصاحب الشقة).

**Prompt Builder**

- Purpose: تركيب الـ Prompt النهائي المرسل للـ LLM.
- Input: Context، نتيجة Tool، رسالة المستخدم الحالية.
- Output: نص الـ Prompt جاهز للإرسال.
- Responsibility: الحفاظ على ترتيب وبنية ثابتة للـ Prompt (انظر قسم Prompt Strategy).

**Response Generator**

- Purpose: توليد الرد النهائي بلغة طبيعية.
- Input: الـ Prompt النهائي.
- Output: نص الرد الجاهز للإرسال للضيف.
- Responsibility: الالتزام بقواعد الرد المحددة في AI Prompt Rules.

**Memory Manager**

- Purpose: إدارة حفظ واسترجاع سجل المحادثة.
- Input: الرسالة الواردة والرد الصادر.
- Output: تحديث جدول Message و Conversation.
- Responsibility: توفير سياق كافٍ للرسائل القادمة دون تحميل بيانات زائدة.

---

## 19. Intent Mapping

| Intent            | Tool                | Priority | Example                          |
| ------------------ | -------------------- | --------- | ---------------------------------- |
| Restaurant           | Restaurant Tool        | Normal      | "فين اقرب مطعم كشري؟"                  |
| Cafe                 | Restaurant Tool        | Normal      | "في كافيه قريب مني؟"                     |
| Tourism              | Knowledge Tool         | Normal      | "ايه اماكن سياحية قريبة؟"                    |
| Weather              | Weather Tool           | Normal      | "الجو النهارده عامل ايه؟"                       |
| House Information    | Knowledge Tool         | Normal      | "الواي فاي كلمة السر ايه؟"                       |
| Complaint            | Complaint Tool         | High        | "في مشكلة في السخان"                                |
| Greeting             | General Chat Tool      | Low         | "السلام عليكم"                                        |
| General Question     | General Chat Tool      | Low         | "ممكن تساعدني؟"                                         |

---

## 20. Tool Contracts

### Restaurant Tool

- **Purpose**: البحث عن مطاعم وكافيهات قريبة من الشقة.
- **Input**: نوع الطلب (مطعم/كافيه)، الموقع الجغرافي للشقة.
- **Output**: قائمة أماكن مع الاسم والعنوان والتقييم إن وُجد.
- **Possible Errors**: فشل الاتصال بـ Google Maps API، عدم وجود نتائج.
- **Dependencies**: Google Maps API.
- **Timeout**: 10 ثوانٍ. إذا تجاوز الاستدعاء المهلة، يتم إيقاف الطلب واعتباره فشلاً (نفس معالجة "فشل الاتصال بـ Google Maps API")، ويُرسل للضيف رد اعتذار مناسب.
- **Example Response**:

```json
{
  "success": true,
  "data": {
    "places": [
      { "name": "مطعم كشري التحرير", "address": "شارع النيل", "rating": 4.5 }
    ]
  }
}
```

### Weather Tool

- **Purpose**: جلب حالة الطقس الحالية.
- **Input**: إحداثيات الشقة.
- **Output**: درجة الحرارة، الوصف، نسبة الرطوبة.
- **Possible Errors**: فشل OpenWeather API، انتهاء الحصة المجانية.
- **Dependencies**: OpenWeather API.
- **Timeout**: 10 ثوانٍ. عند تجاوز المهلة يُعامل الطلب كفشل في OpenWeather API، ويتم إرسال اعتذار للضيف بدلاً من الانتظار.
- **Example Response**:

```json
{
  "success": true,
  "data": { "temperature": 28, "description": "مشمس", "humidity": 40 }
}
```

### Knowledge Tool

- **Purpose**: الإجابة عن أسئلة تخص الشقة والأماكن السياحية المعروفة مسبقاً.
- **Input**: نص السؤال.
- **Output**: نص إجابة من قاعدة معرفة ثابتة.
- **Possible Errors**: عدم توفر إجابة مطابقة.
- **Dependencies**: ملف المعرفة الخارجي (`knowledge.json` أو `knowledge.md`)، بدلاً من بيانات ثابتة داخل الكود (انظر قسم Knowledge Source).
- **Timeout**: 10 ثوانٍ. عند تجاوز المهلة (مثلاً بطء قراءة الملف) يتم اعتبار الإجابة غير متوفرة وتحويل الطلب لصاحب الشقة.
- **Example Response**:

```json
{
  "success": true,
  "data": { "answer": "كلمة سر الواي فاي مكتوبة على الراوتر." }
}
```

### Complaint Tool

- **Purpose**: تسجيل شكوى الضيف وإشعار المالك.
- **Input**: نص الشكوى، guest_id.
- **Output**: تأكيد إنشاء Notification.
- **Possible Errors**: فشل الحفظ في قاعدة البيانات.
- **Dependencies**: Database، Owner Notification Tool.
- **Timeout**: 10 ثوانٍ. عند تجاوز المهلة يتم اعتبار العملية فاشلة وإعادة المحاولة مرة واحدة قبل تسجيل الخطأ.
- **Example Response**:

```json
{
  "success": true,
  "data": { "notification_id": 12, "status": "created" }
}
```

### Owner Notification Tool

- **Purpose**: إرسال تنبيه لصاحب الشقة.
- **Input**: محتوى التنبيه، الأولوية.
- **Output**: تأكيد إرسال التنبيه.
- **Possible Errors**: فشل إرسال الرسالة عبر WhatsApp للمالك.
- **Dependencies**: WhatsApp Cloud API.
- **Timeout**: 10 ثوانٍ. عند تجاوز المهلة يُسجَّل الخطأ ويُعاد المحاولة مرة واحدة، وإذا استمر الفشل يُحفظ التنبيه بحالة "pending" لإعادة المحاولة لاحقاً.
- **Example Response**:

```json
{
  "success": true,
  "data": { "sent": true }
}
```

### General Chat Tool

- **Purpose**: التعامل مع التحيات والأسئلة العامة التي لا تحتاج أداة متخصصة.
- **Input**: نص الرسالة.
- **Output**: رد عام مناسب.
- **Possible Errors**: لا يوجد أخطاء خارجية مرتبطة (لا يعتمد على API خارجي).
- **Dependencies**: LLM فقط.
- **Timeout**: 10 ثوانٍ (يتبع مهلة استدعاء LLM نفسها). عند تجاوز المهلة يتم إرسال رسالة اعتذار مؤقتة للضيف.
- **Example Response**:

```json
{
  "success": true,
  "data": { "reply": "أهلاً بيك، أقدر أساعدك في ايه؟" }
}
```

---

## 21. Prompt Strategy

يتم بناء الـ Prompt النهائي وفق ترتيب ثابت:

```text
System Prompt

*

Guest Information

*

Conversation Summary

*

Tool Result

*

Current User Message
```

سبب استخدام هذا الترتيب:

- **System Prompt** يوضع أولاً لتثبيت القواعد العامة (اللغة، الأسلوب، عدم اختراع معلومات).
- **Guest Information** توفر سياق شخصي (الاسم، تواريخ الإقامة) دون تكرار سؤال الضيف عنها.
- **Conversation Summary** تمنع فقدان السياق في المحادثات الطويلة دون إرسال كامل السجل.
- **Tool Result** يوضع قبل رسالة المستخدم مباشرة ليعتمد الرد عليه كمصدر حقيقي للمعلومات.
- **Current User Message** توضع أخيراً لأنها السؤال الذي يجب الرد عليه مباشرة.

هذا الترتيب الثابت يسهل الصيانة ويقلل الأخطاء عند تعديل أي جزء من الـ Prompt مستقبلاً.

---

## 22. AI Prompt Rules

- الرد بنفس لغة المستخدم.
- عدم اختراع معلومات.
- الاعتماد على نتائج الأدوات.
- الرد باختصار.
- عند عدم المعرفة يتم تحويل الطلب لصاحب الشقة.

---

## 23. Error Handling

| Scenario             | Action                     |
| --------------------- | --------------------------- |
| Weather API Failure     | الاعتذار للمستخدم              |
| Maps API Failure        | اقتراح التواصل مع المالك          |
| OpenAI Failure           | إرسال رسالة اعتذار مؤقتة            |

---

## 24. Error Codes

| Code | Description          | Suggested Action                     |
| ---- | --------------------- | -------------------------------------- |
| 1001 | Guest Not Found         | التحقق من رقم الهاتف والتسجيل             |
| 1002 | Weather API Failed      | إعادة المحاولة أو الاعتذار للمستخدم           |
| 1003 | Maps API Failed         | إعادة المحاولة أو اقتراح التواصل مع المالك      |
| 1004 | OpenAI Failed           | إرسال رسالة اعتذار مؤقتة وتسجيل الخطأ             |
| 1005 | WhatsApp Failed         | إعادة المحاولة وتسجيل الخطأ                        |
| 1006 | Invalid Request         | إرجاع رسالة خطأ واضحة للمرسل                          |

---

## 25. Environment Variables

| Variable             | Required | Description                          | Default             |
| --------------------- | -------- | -------------------------------------- | -------------------- |
| OPENAI_API_KEY          | Yes        | مفتاح الوصول إلى OpenAI API                | -                      |
| WHATSAPP_TOKEN          | Yes        | Token الخاص بـ WhatsApp Cloud API           | -                      |
| VERIFY_TOKEN            | Yes        | Token للتحقق من الـ Webhook                     | -                      |
| PHONE_NUMBER_ID         | Yes        | معرف رقم الهاتف في WhatsApp Business             | -                      |
| DATABASE_URL            | Yes        | رابط الاتصال بقاعدة البيانات                          | sqlite:///./app.db      |
| GOOGLE_MAPS_API_KEY     | Yes        | مفتاح Google Maps API                                  | -                      |
| WEATHER_API_KEY         | Yes        | مفتاح OpenWeather API                                    | -                      |
| LOG_LEVEL               | No         | مستوى تسجيل الأحداث                                         | INFO                    |
| ENVIRONMENT             | No         | بيئة التشغيل (development/production)                          | development              |
| MODEL_NAME              | No         | اسم موديل الـ LLM المستخدم                                        | gpt-4o-mini              |
| TEMPERATURE             | No         | درجة العشوائية في رد الـ LLM                                       | 0.3                      |
| MAX_TOKENS              | No         | الحد الأقصى لطول رد الـ LLM                                        | 500                      |

يجب عدم كتابة هذه القيم بشكل ثابت (hardcoded) داخل الكود، لأنها قد تحتاج تعديلاً متكرراً أثناء التجربة والتطوير (مثل تجربة موديل مختلف أو تقليل التكلفة)، ووضعها كمتغيرات بيئة يسمح بتغييرها دون تعديل الكود أو إعادة النشر.

---

## 26. Configuration Strategy

- كل الإعدادات تُحمَّل عبر `config.py` فقط.
- `config.py` هو المكان الوحيد الذي يقرأ من `.env` باستخدام `os.getenv()`.
- لا يجوز لأي ملف آخر في المشروع استدعاء `os.getenv()` مباشرة.
- باقي أجزاء التطبيق (services، agent، api، scheduler...) تستورد الإعدادات من `config.py` فقط، ولا تتعامل مع `.env` بشكل مباشر.

هذه القاعدة إلزامية في المشروع، والهدف منها ضمان مصدر واحد موثوق (single source of truth) للإعدادات، وتسهيل تتبع أي متغير بيئة يُستخدم في الكود، وتقليل الأخطاء الناتجة عن قراءة نفس المتغير بطرق مختلفة في أكثر من مكان.

---

## 27. Coding Rules

- No business logic inside API routes.
- Services contain application logic.
- One responsibility per Tool.
- Configuration only inside `config.py`.
- No hardcoded secrets.
- Always validate user input.
- Always log unexpected exceptions.
- Keep functions small and focused.
- Prefer dependency injection where appropriate.
- Keep naming consistent.
- Avoid duplicated code.

---

## 28. Logging Strategy

يتم تسجيل:

- Incoming requests (الرسائل الواردة).
- Outgoing responses (الردود الصادرة).
- LLM usage (عدد الاستدعاءات واستهلاك التوكنز إن أمكن).
- Tool execution (اسم الأداة والنتيجة).
- Errors (الأخطاء).
- Warnings (التحذيرات).
- Scheduler events (تنفيذ المهام الدورية).
- Owner notifications (التنبيهات المرسلة لصاحب الشقة).

يُفضّل الاحتفاظ بالسجلات بصيغة منظمة (structured logging) لتسهيل المراجعة لاحقاً، مع الالتزام بعدم تسجيل بيانات حساسة (مثل مفاتيح الـ API).

بالإضافة إلى ذلك، يُنشأ **Request ID** فريد لكل رسالة/محادثة واردة، ويُرفق مع كل سطر Log متعلق بهذا الطلب (من استقبال الرسالة وحتى إرسال الرد). هذا يسهّل تتبع دورة حياة الطلب بالكامل عبر مختلف المكونات (Validation، Intent Detection، Tool Execution، LLM) عند تصحيح الأخطاء.

---

## 29. Scheduler Details

| Job                | Trigger Condition                              |
| -------------------- | ------------------------------------------------ |
| Welcome Message        | يفحص الضيوف الذين تاريخ وصولهم اليوم، حسب الجدولة المحددة في Config    |
| Checkout Reminder      | يفحص الضيوف الذين يغادرون خلال 24 ساعة، حسب الجدولة المحددة في Config     |
| Goodbye Message        | يفحص الضيوف الذين تاريخ مغادرتهم اليوم، حسب الجدولة المحددة في Config       |
| Review Request         | يُرسل بعد رسالة الوداع مباشرة بفارق زمني بسيط                   |
| Cleanup Job            | يحدّث حالة الضيوف المكتملين إلى Completed، حسب الجدولة المحددة في Config              |

بدلاً من تثبيت فترة التشغيل (مثل "كل ساعة") داخل الكود، يتم تحديد جدول كل Job عبر `config.py`، إما كـ Cron expression (مثال: `0 * * * *` لتشغيلها كل ساعة) أو كفترة زمنية قابلة للتعديل (interval بالدقائق/الساعات). هذا يسمح بتغيير توقيت أي Job دون تعديل الكود، حسب احتياج المشروع الفعلي بعد التشغيل.

---

## 30. Future Improvements

الميزات التالية مستبعدة عمداً من الإصدار 1.0، وسيتم النظر فيها لاحقاً:

- Dashboard
- Voice Messages
- Image Understanding
- Multi Apartment
- Multi Owner
- Booking Integration
- Analytics Dashboard
- Multi Language
- Payment Integration
- Knowledge Base Expansion

---

## 31. Development Plan

الترتيب المقترح لتنفيذ المشروع:

1. [ ] Project Setup
2. [ ] Configuration
3. [ ] Database
4. [ ] Models
5. [ ] Guest Registration
6. [ ] WhatsApp Integration
7. [ ] Conversation Storage
8. [ ] AI Agent
9. [ ] Weather Tool
10. [ ] Restaurant Tool
11. [ ] Knowledge Tool
12. [ ] Complaint Tool
13. [ ] Scheduler
14. [ ] Testing
15. [ ] Deployment

سبب هذا الترتيب أنه يبني كل خطوة على أساس جاهز من الخطوة السابقة، ويقلل التعقيد: تجهيز المشروع والإعدادات (Configuration) أولاً حتى لا يُعاد تعديلها لاحقاً، ثم قاعدة البيانات والـ Models كأساس تخزين البيانات، ثم تسجيل الضيوف وربط WhatsApp لأن باقي الميزات تعتمد عليهما، ثم حفظ المحادثات (Conversation Storage) كأساس للسياق، ثم الـ AI Agent كطبقة تنسيق عامة، ثم الأدوات (Weather، Restaurant، Knowledge، Complaint) كل واحدة على حدة لتقليل الأخطاء المتزامنة، ثم الجدولة (Scheduler) بعد استقرار المنطق الأساسي، وأخيراً الاختبار والنشر.
