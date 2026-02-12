# Review of "How Fast Can I Run My VLA? Demystifying VLA Inference Performance with VLA-Perf"

## 1. Summary

This paper presents VLA-Perf, an analytical roofline-based performance model for predicting inference latency and throughput of Vision-Language-Action (VLA) models across diverse hardware and deployment configurations. The authors systematically explore the VLA inference performance landscape, examining model design choices (scaling, architecture, context length, denoising steps, asynchronous execution) and system deployment options (on-device, edge-server, cloud-server). Through their analysis, they distill 15 key takeaways intended to guide future VLA model and system design for real-time robotics applications. The work addresses a genuine gap in understanding how VLA inference performance varies across the combinatorial space of models and systems.

## 2. Strengths

**S1. Timely and Practically Important Problem**
The question of real-time VLA inference is genuinely critical for embodied AI deployment. As someone who has watched the field evolve from hand-crafted features to modern foundation models, I appreciate that this work treats inference performance as a first-class concern rather than an afterthought. The framing around 10 Hz (acceptable) and 100 Hz (high-performance) targets provides concrete, actionable benchmarks.

**S2. Systematic Coverage of the Design Space**
The paper admirably covers a wide range of configurations: model scaling, long-context inference, diffusion vs. autoregressive architectures, action chunking, asynchronous execution, dual-system pipelines, and various deployment scenarios. This breadth is valuable for practitioners making design decisions.

**S3. Analytical Modeling Approach**
The choice to use analytical performance modeling rather than exhaustive empirical evaluation is pragmatic and well-justified. The roofline model is a principled approach, and the validation against real Triton implementations (73-83% accuracy) provides reasonable confidence in the predictions.

**S4. Clear Presentation of Takeaways**
The 15 numbered takeaways provide digestible guidance. The paper is well-organized, with clear figures and tables that effectively communicate the key findings.

**S5. Open-Source Commitment**
The commitment to release VLA-Perf enables the community to extend this analysis to new models and systems, which is valuable for the rapidly evolving field.

## 3. Weaknesses

**W1. Validation is Limited and Potentially Optimistic**
The validation against only one implementation (Ma et al.'s Triton-based π0 on RTX 4090) is insufficient. The 73-83% accuracy claim is based on a single model, single hardware platform, and a highly optimized implementation. How does accuracy vary across:
- Different model architectures (autoregressive vs. diffusion)?
- Different hardware (edge GPUs, datacenter GPUs)?
- Less optimized implementations that practitioners might actually use?

The paper acknowledges that VLA-Perf estimates upper bounds, but this optimism could mislead practitioners. A 20-30% gap between predicted and achievable performance is substantial when targeting real-time constraints.

**W2. Missing Real-World System Complexity**
The paper abstracts away critical real-world factors:
- **Sensor latency**: Camera capture and preprocessing can add 10-50ms depending on the pipeline
- **Robot execution latency**: Actuator response times vary significantly across platforms
- **Memory management**: KV cache management, memory fragmentation, and allocation overhead
- **Thermal throttling**: Edge devices like Jetson Thor will throttle under sustained load
- **Multi-robot scenarios**: What happens when multiple robots share inference infrastructure?

These factors can dominate end-to-end latency in practice. The paper's focus on pure inference latency, while useful, may give an incomplete picture.

**W3. Network Modeling is Oversimplified**
The network model (Equation 4) assumes constant bandwidth and latency, which doesn't reflect real wireless networks:
- WiFi and cellular networks exhibit high variance in latency and bandwidth
- Packet loss and retransmission are not modeled
- Network congestion from other traffic is ignored
- The "base latency" values in Table 7 seem optimistic (e.g., 2.5ms for WiFi 7)

For mobile robots relying on wireless connectivity, this oversimplification could lead to significant prediction errors.

**W4. Limited Architectural Diversity**
The evaluation focuses almost exclusively on π0 variants. While π0 is a reasonable choice, the VLA landscape includes:
- Pure autoregressive models (RT-2, OpenVLA)
- Different vision encoders (CLIP, DINOv2, EVA)
- Different VLM backbones (PaLM, LLaMA, Qwen)
- Hybrid architectures with specialized components

The generalizability of findings to these architectures is unclear.

**W5. Accuracy-Performance Tradeoffs are Ignored**
The paper explicitly states it focuses on performance "under the assumption that the underlying models meet the necessary accuracy thresholds." However, many of the design choices analyzed (fewer denoising steps, smaller models, quantization) directly impact task success rates. Without understanding these tradeoffs, practitioners cannot make informed decisions.

**W6. Missing Statistical Rigor**
The paper presents point estimates without confidence intervals or sensitivity analysis. How robust are the takeaways to:
- Variations in hardware specifications (e.g., memory bandwidth variance)?
- Different operator implementations?
- Model configuration variations?

**W7. Dual-System Analysis is Speculative**
The dual-system evaluation (§4.10) acknowledges making "approximations" due to lack of open-source implementations. The assumptions about System 1/System 2 interaction may not reflect actual implementations, limiting the practical value of these findings.

## 4. Questions for Authors

1. **Validation breadth**: Can you validate VLA-Perf against additional implementations, particularly on edge hardware (Jetson) and with autoregressive models? What is the expected accuracy range across different scenarios?

2. **Real-world deployment**: Have you validated any predictions against actual robot deployments? How do sensor latency, robot execution time, and thermal effects impact end-to-end performance?

3. **Network variability**: How sensitive are your server-side inference conclusions to network variance? What happens when WiFi latency spikes to 50-100ms (common in practice)?

4. **Accuracy tradeoffs**: For the model scaling analysis (§4.3), what are the corresponding accuracy implications? Is a 70B model actually better than a 2B model for manipulation tasks?

5. **Memory constraints**: Your analysis assumes models fit in memory. How do your conclusions change when memory becomes a constraint (e.g., long-context inference on RTX 4090)?

6. **Batch inference**: You focus on batch size 1. How do conclusions change for multi-robot deployments sharing inference infrastructure?

7. **Failure modes**: When does VLA-Perf's predictions break down? What are the scenarios where the roofline model is most inaccurate?

8. **Quantization**: You mention quantization as a technique but don't analyze it. How do INT8/INT4 quantization affect your performance landscape?

## 5. Detailed Comments

### Section 1 (Introduction)
- The framing is clear and motivating. The 10 Hz / 100 Hz targets are helpful anchors.
- The claim that "executing the same VLA model across different inference systems can lead to performance differences of multiple orders of magnitude" is compelling but would benefit from early evidence.

### Section 2 (Background)
- Good coverage of VLA architectures and efficiency techniques.
- The research gap articulation is clear.

### Section 3 (VLA-Perf)
- **Equation 1-4**: The formulation is standard roofline modeling. However, the assumption that "local data movement on the same accelerator is sufficiently fast to be treated as negligible" may not hold for large KV cache transfers.
- **Table 1**: The validation is encouraging but limited. The accuracy improvement from 73.3% to 82.6% with more cameras suggests the model is more accurate for compute-bound workloads. What about memory-bound scenarios?
- The acknowledgment that "68-75% of roofline-model-predicted performance can be achieved on real systems" (citing Ma et al.) seems inconsistent with your 73-83% claim. Please clarify.

### Section 4 (Evaluation)
- **§4.2 (Baseline)**: Table 4's compute/memory-bound analysis is insightful. The observation that Jetson Thor is memory-bound even for vision/VLM due to LPDDR is important.

- **§4.3 (Scaling)**: The linear scaling observation (Takeaway 3) is expected but useful to confirm. However, the claim that "datacenter GPUs can support real-time inference for VLA models that are more than one order of magnitude larger" (Takeaway 4) needs accuracy context. Is a 70B VLA actually useful?

- **§4.4 (Long-Context)**: The finding that 1K timesteps is feasible on B100 is interesting. However, how does KV cache memory scale? Table 6 shows 13.2 GB for 1K steps—this seems to assume efficient memory management.

- **§4.5 (Denoising/Chunking)**: Takeaway 6 (denoising steps matter, chunk size doesn't) is actionable. Figure 6c nicely explains why through operator intensity analysis.

- **§4.6 (Diffusion vs. Autoregressive)**: The 102.4× speedup claim for diffusion over autoregressive (Takeaway 7) is striking. However, this comparison may be unfair—autoregressive models often use different architectures optimized for sequential generation. The parallel decoding comparison is more informative.

- **§4.7 (On-Device vs. Server)**: Takeaway 9 is important for practitioners. However, the conclusion that "server-side inference significantly outperforms on-device inference in most scenarios" may not account for reliability concerns in real deployments.

- **§4.8 (Collaborative)**: Takeaway 10 (device-server collaboration is "generally unattractive") is surprising and counterintuitive. This deserves more investigation—are there configurations where collaboration makes sense?

- **§4.9 (Asynchronous)**: The asynchronous inference analysis is valuable. However, the paper doesn't discuss the control-theoretic implications of acting on stale observations. What's the acceptable staleness for manipulation tasks?

- **§4.10 (Dual-System)**: As noted, this section is speculative. The approximations made should be more clearly flagged as limitations.

- **§4.11 (100 Hz)**: This section effectively synthesizes the findings. The practical guidance is clear.

### Writing Quality
- Generally clear and well-organized.
- Some redundancy between sections could be reduced.
- The paper would benefit from a limitations section beyond the brief mention in the conclusion.

### Figures and Tables
- Figure 1 effectively summarizes the paper's scope.
- Tables 3-4 are informative.
- Figure 6 is well-designed and clearly communicates the denoising/chunking tradeoffs.
- Figure 8-9 effectively compare deployment scenarios.

### Minor Issues
- The GitHub link is a TODO placeholder.
- Table 1 caption mentions "empty language prompt"—how does prompt length affect accuracy?
- The paper uses "performant" which some consider non-standard.

## 6. Recommendation

**Overall Score: 5/10 (Borderline)**

**Confidence: High**

### Justification

This paper addresses an important and timely problem—understanding VLA inference performance is crucial as the field moves toward real-world deployment. The systematic exploration of the design space and the 15 takeaways provide genuine value to practitioners.

However, several significant concerns prevent a stronger recommendation:

1. **Limited validation**: The roofline model is validated against only one implementation on one hardware platform. For a paper whose core contribution is a performance modeling tool, this is insufficient. The community needs confidence that VLA-Perf's predictions generalize.

2. **Oversimplified assumptions**: The abstractions around network behavior, memory management, and system-level effects may lead to predictions that don't reflect real deployments. For robotics applications where reliability matters, this is concerning.

3. **Missing accuracy context**: The complete separation of performance from accuracy makes the practical guidance incomplete. Practitioners need to understand tradeoffs, not just performance in isolation.

4. **Speculative sections**: The dual-system analysis relies on assumptions that may not reflect actual implementations.

The paper would be significantly strengthened by:
- Broader validation across hardware platforms and model architectures
- Sensitivity analysis showing robustness of conclusions
- At least qualitative discussion of accuracy-performance tradeoffs
- Real-world deployment validation, even if limited

As it stands, the paper provides useful directional guidance but the quantitative predictions should be treated with caution. I would encourage the authors to address the validation concerns and resubmit—the core contribution is valuable, but the execution needs strengthening.

---

*This review reflects my perspective that AI systems research must be grounded in real-world applicability. The VLA inference problem is genuinely important, and I appreciate the authors' systematic approach. However, for work that aims to guide practitioners, we must ensure our predictions are reliable across the diverse conditions of actual deployment.*