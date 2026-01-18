# AI Incident Resolution Copilot 🚨🤖

An enterprise-grade, multi-agent AI system that analyzes production incidents, retrieves similar historical incidents using semantic search (RAG), and generates structured resolution and escalation plans.

This project demonstrates **agentic AI**, **retrieval-augmented generation (RAG)**, and **enterprise AI system design** using Python.

---

## 🔍 Problem Statement

In large organizations, incident resolution is slow because knowledge is scattered across past tickets, documents, and individual experience.

This project builds an **AI-powered Incident Resolution Copilot** that:
- Understands a new incident
- Retrieves similar past incidents by meaning (not keywords)
- Generates a step-by-step fix plan
- Assesses business risk and escalation needs

---

## 🧠 Architecture Overview

- **Analyzer Agent** – Understands and classifies the incident
- **Knowledge Retriever Agent** – Retrieves similar historical incidents (RAG)
- **Resolution Planner Agent** – Creates fix, validation, and rollback plans
- **Risk & Escalation Agent** – Assesses severity and escalation

**Memory Layer**
- Sentence Transformers (embeddings)
- FAISS (vector database)

---

## 🧰 Tech Stack

- Python
- CrewAI (multi-agent orchestration)
- FAISS (semantic search)
- Sentence Transformers
- Retrieval-Augmented Generation (RAG)

All components run locally using free resources.

---

## 📂 Project Structure

