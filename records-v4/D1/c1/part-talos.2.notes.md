# Part 2 classification notes

Scope: zero-based input indices 92–212 inclusive, 121 rows. Only the fixed text, sentence list, fact index, assigned input, its raw inventory and official public source/documentation were consulted.

## Rule N: in-memory network resources

S8.2-5: “What exists only while the computer runs—a process, an open port, a mount point, a relationship between services—is not considered a separate object: it belongs to the program or setting that creates it, and the decision follows that for the program or setting.”

Rows 92–144 represent API resource instances in the network namespace, not the persistent machine-configuration source. All are RUNTIME. Their raw metadata identifies the creating merge/status controller. The controller runs within machined. Its own installed/program classification remains UNKNOWN because packaged-file integrity was not established; this does not change the resource instance's RUNTIME decision.

Official source matching the observed v1.14.6 version: https://raw.githubusercontent.com/siderolabs/talos/v1.14.6/internal/app/machined/pkg/runtime/v1alpha2/v1alpha2_state.go . NewState selects `inmem.NewStateWithOptions` for each namespace. The namespace registration explicitly includes network and network-config. The resource registration includes each inspected spec/status class. This establishes resource-instance lifetime separately from unknown stored-file persistence in FACTS.md.

Manual checks: read the complete raw metadata/spec of the following ten input rows, matching id and owner. Three LinkSpecs and the loopback AddressSpec have default layers; two physical AddressSpecs and two RouteSpecs have operator layers; the DNS forwarding AddressSpec and ResolverSpec also have operator layers. No operator label was treated as evidence of a human choice. All ten are merged in-memory objects.

- talos-6998c9d70456b15188cbe45a
- talos-bf5eb87a0976ac7dfdb8bbad
- talos-3a372dbbd8996d951d2d9ff6
- talos-846c6d9627d5b430af7382a7
- talos-ab374453e69e6dcf4c90aca8
- talos-26b02098e721b15ae85cc44e
- talos-c53c0d03e040c6ad4e14d59a
- talos-580f529f02d78acb23c0b7ad
- talos-37f5b08127cb39525bcde935
- talos-07fd45398afa808b12852ac0

## Rule S: live sockets

S8.2-5 explicitly excludes open ports as separate objects. Rows 145–210 are live TCP/UDP socket observations; all are RUNTIME regardless of owner. The raw netstat columns omit process identifiers, so endpoints alone do not establish arbitrary client ownership. Unknown ownership and inherited decision are stated without converting a certainly ephemeral socket into a separate UNKNOWN object.

Official constants for v1.14.6 identify documented server ports: https://raw.githubusercontent.com/siderolabs/talos/v1.14.6/pkg/machinery/constants/constants.go . Relevant literal assignments: `EtcdClientPort = 2379`, `EtcdPeerPort = 2380`, `EtcdClientHTTPPort = 2383`, `KubeletPort = 10250`, `ApidPort = 50000`, `TrustdPort = 50001`, `DefaultKubePrismPort = 7445`. Together with running-service observations these support the stated server roles, but do not establish client owners. Package integrity and derived coverage of the creator remain unknown.

Official host DNS documentation: https://docs.siderolabs.com/talos/v1.14/networking/host-dns . It states the resolver listens on 127.0.0.53:53 using TCP and UDP; DNS forwarding allocates 169.254.116.108. Its enablement can be default or explicitly selected, so no particular source-setting decision is presumed.

Manual checks: compared the following ten input rows with raw/0019-talos-ports.out. Verified listen states at the two DNS addresses, arbitrary local listeners, kubelet health listener, KubePrism listener, established connections and TIME_WAIT. Each remains live socket state; no owner was inferred from a remote endpoint alone.

- talos-d8c29fedf733e0a4a51ba28e
- talos-54afd7caa5900923ae1dfd8c
- talos-555a2e3a32a654473a1432af
- talos-2bfebb9ec925a4d41df41abe
- talos-04dfc8d284fa6b7475781e80
- talos-a78300a1c6acec3a99072b47
- talos-e4281c282fe155a27501bfb8
- talos-6c9033b76edb05447045f278
- talos-c8ba828a7254100ad6de102d
- talos-380f8868bcaa19b810085ca0

## Individual container cases

Rows 211 and 212 were read individually from raw/0020-talos-containers.out and cross-checked against raw/0008-talos-processes.out. They identify RUNNING apid and trustd instances with PIDs, rather than image packages. The containerd shim command lines name these instances. S8.2-5 therefore gives RUNTIME; executable contents remain separately classifiable under S8.2-7/9/22. Containerd's own classification is UNKNOWN because file integrity is unknown.

Validation: 121 assigned input IDs, 121 output IDs, exactly equal with no duplicates. All decisions RUNTIME. Text word limits checked during writing. No stored-object persistence assumptions were introduced.
