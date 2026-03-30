# NeuroCore Prompting Strategy

This document explains how I structure prompts when working with ChatGPT during the development of NeuroCore.

This isn’t just convenience — this is part of how NeuroCore is being built.

---

# Purpose

The goal of structured prompting is to:

- maintain continuity between sessions  
- provide accurate system context  
- reduce repeated explanations  
- accelerate development progress  

---

# Core Idea

ChatGPT does not retain persistent memory across sessions.

To compensate for this, I provide:

- system context  
- architecture details  
- current state information  
- development goals  

This allows the assistant to operate as if it has ongoing awareness of the NeuroCore system.

---

# Prompt Structure

A good prompt should include:

- what NeuroCore is  
- what the current environment looks like  
- what has already been built  
- what the current goal is  

---

# Why This Matters

Without structured prompting:

- responses become generic  
- system-specific context is lost  
- development becomes inefficient  

With structured prompting:

- responses are aligned with the actual system  
- development stays consistent  
- the assistant behaves like a knowledgeable collaborator  

---

# Long-Term Vision

NeuroCore should eventually be able to:

- understand its own architecture  
- reason over its own documentation  
- assist with its own development  
- guide troubleshooting workflows  

This document helps establish the foundation for that capability.