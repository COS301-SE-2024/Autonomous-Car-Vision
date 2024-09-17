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

    let nodes = [];

    onMount(async () => {
        try {
            // Fetch user data
            const userResponse = await axios.post("http://localhost:8000/getCorporationUsersID/", {
                uid: window.electronAPI.getUid(),
            });
            let users = userResponse.data.users;
            let userIDS = [];
            for (let i = 0; i < users.length; i++) {
                userIDS.push(users[i].uid);
            }
                
            let agentsArray = [];
            for (let i = 0; i < userIDS.length; i++) {
                const agentResponse = await axios.post("http://localhost:8000/getAllAgentsForUser/", {
                    uid: userIDS[i],
                });
                let agents = agentResponse.data.agents;
                agentsArray.push(agents);
            }
            let agents = agentsArray[0];
            for (let i = 0; i < agents.length; i++) {
                for (let j = 0; j < agents.length; j++) {
                    if(i == j){
                        continue;
                    }
                    if (agents[i].aid === agents[j].aid && agents[i].uid === agents[j].uid) {
                        agents.splice(j, 1);
                    }
                }
            }
            console.log("User IDS:", userIDS);
            console.log("Agents:", agents);
            
            // Process data and create nodes
            nodes = makeNodes({ clients: users, agents: agents });

            // Update the writable stores
            TeamAgents.set(agents.map(() => false));
            TeamClients.set(users.map(() => false));
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    });


    function makeNodes(JsonPayload) {
        let NodesMake = [];

        // Create Broker node
        let brokerNode = {
            id: "10000",
            type: "Broker",
            position: { x: 100, y: -200 },
            label: "Broker",
            anchors: [
                { id: "in1", type: "input" }, // Input for Agents
            ],
            agents: JsonPayload.agents.map((agent) => agent.id.toString()),
            booleanID: 0,
        };
        NodesMake.push(brokerNode);

        // Step 2: Create Agent nodes and connect them to the Broker
        let agentCount = 1;
        // Create Agent nodes
        JsonPayload.agents.forEach((agent, index) => {
            let agentNode = {
                id: agent.aid.toString(),
                type: "Agent",
                position: { x: index * 200 - 500, y: -500 }, // Adjust positions dynamically
                label: `Agent ${agent.aid.toString()}`,
                anchors: [
                    { id: "out1", type: "output", out: "10000" }, // Connected to Broker
                ],
                clients: [], // Will populate later with connected clients
                booleanID: agentCount++,
            };
            NodesMake.push(agentNode);
        });

        // Step 3: Create Client nodes and connect them to their respective Agents
        let clientCount = 1;
        // Create Client (User) nodes
        JsonPayload.clients.forEach((client, clientIndex) => {
            let clientNode = {
                id: client.uid.toString(),
                type: "Client",
                position: { x: clientIndex * 300, y: 300 },
                label: client.uname,
                anchors: [{id: "out1", type: "output", out: "10000"}],
                agents: [],
                booleanID: clientCount++
            };

            // Connect clients to agents
            JsonPayload.agents.forEach(agent => {
                clientNode.agents.push(agent.aid.toString());
                let agentNode = NodesMake.find(
                    node => node.id === agent.aid.toString() && node.type === "Agent"
                );
                if (agentNode) {
                    agentNode.clients.push(clientNode.id);
                }
            });

            NodesMake.push(clientNode);
        });
        console.log("NodesMake:", NodesMake);
        return NodesMake;
}

</script>

<ProtectedRoutes>
    {#if nodes.length == 0}
        <div>Loading...</div>
    {:else}
    <Svelvet TD fitView theme="dark" edgeStyle="bezier">
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
                    dimensions={{ width: 150, height: 100 }}
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
                    dimensions={{ width: 150, height: 100 }}
                    nodeData={node}
                />
            {/if}
        {/each}
    </Svelvet>
    {/if}
</ProtectedRoutes>
<style>
    /* Add any necessary styles */
</style>