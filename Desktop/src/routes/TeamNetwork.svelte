<script>
    import ProtectedRoutes from "./ProtectedRoutes.svelte";
    import { Svelvet } from "svelvet";
    import TeamNode from "../components/TeamNode.svelte";
    import { onMount } from "svelte";
    import { TeamClients, TeamAgents } from "../stores/store";
    import TeamConnectionNodes from "../components/TeamConnectionNodes.svelte";
    import BrokerNode from "../components/BrokerNode.svelte";
    import ManagerNode from "../components/ManagerNode.svelte";
    import axios from "axios";
    import CryptoJS from "crypto-js";
    import Spinner from "../components/Spinner.svelte";
    import { theme } from "../stores/themeStore";

    let nodes = [];
    let HOST_IP;
    let agentsGlobal = [];
    let themeMaterial = "dark";

    let users = [];
    let teamName = "Team";

    onMount(async () => {
        HOST_IP = await window.electronAPI.getHostIp();

        try {
            const response = await axios.post(
                "http://" + HOST_IP + ":8000/getTeamName/",
                {
                    uid: window.electronAPI.getUid(),
                },
            );
            teamName = response.data.teamName;
        } catch (error) {
            console.error(error);
        }

        try {
            const response = await axios.post(
                "http://" + HOST_IP + ":8000/getTeamMembers/",
                {
                    uid: window.electronAPI.getUid(),
                },
            );
            users = response.data.teamMembers.sort((a, b) => {
                if (a.is_admin === b.is_admin) return 0;
                return a.is_admin ? -1 : 1;
            });
        } catch (error) {
            console.error(error);
        }

        try {
            // Fetch user data
            const userResponse = await axios.post(
                "http://" + HOST_IP + ":8000/getCorporationUsersID/",
                {
                    uid: window.electronAPI.getUid(),
                },
            );
            let users = userResponse.data.users || []; // Ensure users is an array
            let userIDS = users.map((user) => user.uid); // Extract user IDs

            let agentsArray = [];
            for (let i = 0; i < userIDS.length; i++) {
                const agentResponse = await axios.post(
                    "http://" + HOST_IP + ":8000/getAllAgentsForUser/",
                    {
                        uid: userIDS[i],
                    },
                );
                let agents = agentResponse.data.agents || []; // Ensure agents is an array
                agentsArray.push(...agents); // Combine agents into one array
            }

            agentsGlobal = agentsArray;

            // Step 1: Filter agents - only keep agents if a user has uploaded to them
            // We check if `uid` from the agent matches any in `userIDS`
            const filteredAgents = agentsArray.filter((agent) => {
                return userIDS.includes(agent.uid);
            });

            // Step 2: Remove duplicates based on 'aid' (Agent ID)
            const uniqueAgents = [
                ...new Map(
                    filteredAgents.map((agent) => [agent.aid, agent]),
                ).values(),
            ];

            // Step 3: Process data and create nodes
            nodes = makeNodes({ clients: users, agents: uniqueAgents });

            // Step 4: Update the writable stores

            // Initialize TeamAgents with agent IDs and boolean values
            let agentBoolMap = {};
            uniqueAgents.forEach((agent) => {
                agentBoolMap[agent.aid] = false; // Initialize with false
            });
            TeamAgents.set(agentBoolMap);

            // Initialize TeamClients with client IDs and boolean values
            let clientBoolMap = {};
            users.forEach((client) => {
                clientBoolMap[client.uid] = false; // Initialize with false
            });
            TeamClients.set(clientBoolMap);
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    });

    function makeNodes(JsonPayload) {
        let NodesMake = [];

        // Ensure that agents and clients are available and are arrays
        const agents = JsonPayload.agents || [];
        const clients = JsonPayload.clients || [];

        // Step 1: Create Broker node
        let brokerNode = {
            id: "10000",
            type: "Broker",
            position: { x: 0, y: 0 },
            label: "Broker",
            anchors: [{ id: "in1", type: "input" }], // Input for Agents
            agents: agents.map((agent) => agent.aid.toString()),
            booleanID: 0,
            team_name: teamName
        };
        NodesMake.push(brokerNode);

        // Step 2: Create Agent nodes and connect them to the Broker
        agents.forEach((agent, index) => {
            let agentNode = {
                id: agent.aid.toString(),
                type: "Agent",
                position: { x: index * 200 - 500, y: -500 }, // Adjust positions dynamically
                label: `Agent ${agent.aid.toString()}`,
                anchors: [{ id: "out1", type: "output", out: "10000" }], // Connected to Broker
                clients: [], // Will populate later with connected clients
                booleanID: {
                    // Track boolean state for visualization
                    bool: index,
                    id: agent.aid,
                },
            };
            NodesMake.push(agentNode);
        });

        // Step 3: Create Client nodes and connect them to their respective Agents
        clients.forEach((client, index) => {
            let clientNode = {
                id: client.uid.toString(),
                type: "Client",
                position: { x: index * 350, y: 500 },
                label: client.uname,
                anchors: [{ id: "out1", type: "output", out: "10000" }],
                agents: [],
                booleanID: {
                    bool: index,
                    id: client.uid, // Ensure unique ID for each client
                },
                profilePhoto: null,
            };
            
            // Matching user to profilePhoto
            // Find the user corresponding to the client
            const matchingUser = users.find((user) => user.uid === client.uid);
            // If a matching user is found, generate the Gravatar URL
            if (matchingUser && matchingUser.uemail) {
                clientNode.profilePhoto =
                    "https://www.gravatar.com/avatar/" +
                    CryptoJS.SHA256(matchingUser.uemail.trim().toLowerCase()) +
                    "?d=retro";
            }

            // Collect agent connections and populate clientNode.agents
            agentsGlobal.forEach((agent) => {
                // Check if the agent's uid matches the client's uid
                if (clientNode.id === agent.uid.toString()) {
                    // Add the agent's aid to the clientNode's agents list
                    if (!clientNode.agents.includes(agent.aid.toString())) {
                        clientNode.agents.push(agent.aid.toString());
                    }

                    // Find the agent node in NodesMake
                    let agentNode = NodesMake.find(
                        (node) =>
                            node.id === agent.aid.toString() &&
                            node.type === "Agent",
                    );

                    // If the agentNode exists, connect the client to it
                    if (agentNode) {
                        if (!agentNode.clients.includes(clientNode.id)) {
                            agentNode.clients.push(clientNode.id); // Connect agent to client
                        }
                    }
                }
            });

            NodesMake.push(clientNode);
        });
        return NodesMake;
    }

    theme.subscribe((value) => {
        if (value == "highVizLight") {
            themeMaterial = "light";
        } else {
            themeMaterial = "dark";
        }
    });
</script>

<ProtectedRoutes>
    {#if nodes.length == 0}
        <div class="flex justify-center w-full">
            <Spinner />
        </div>
    {:else}
        <Svelvet TD fitView theme={themeMaterial} edgeStyle="bezier">
            {#each nodes as node}
                {#if node.type == "Agent"}
                    <TeamConnectionNodes
                        id={node.id}
                        position={node.position}
                        dimensions={{ width: 150, height: 100 }}
                        nodeData={node}
                    />
                {:else if node.type == "Broker"}
                    <BrokerNode
                        id={node.id}
                        position={node.position}
                        dimensions={{ width: 250, height: 150 }}
                        nodeData={node}
                    />
                {:else if node.type == "Manager"}
                    <ManagerNode
                        id={node.id}
                        position={node.position}
                        dimensions={{ width: 150, height: 100 }}
                        nodeData={node}
                    />
                {:else}
                    <TeamNode
                        id={node.id}
                        position={node.position}
                        dimensions={{ width: 300, height: 300 }}
                        nodeData={node}
                    />
                {/if}
            {/each}
        </Svelvet>
    {/if}
</ProtectedRoutes>

<style>
</style>
