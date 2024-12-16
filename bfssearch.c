#include<stdio.h>
#include<stdlib.h>
#define SIZE 10

typedef struct node {
    int data;
    int status;
    struct node *next, *point;
} node;

node *q[SIZE]; // to maintain queue
int front = 0, rear = 0; // to store queue
node *g = 0;

// Function to add vertices
void addvertices(int n) {
    node *t = (node *)malloc(sizeof(node));
    t->data = n;
    t->point = 0;
    t->next = g;
    g = t;
}

// Function to find vertex node address of a vertex
node *find(int n) {
    node *t = g;
    while (t != 0 && t->data != n)
        t = t->next;
    return t;
}

// Function to add an edge
void addedge(int u, int v) {
    node *v1, *v2, *t;
    v1 = find(u);
    v2 = find(v);
    t = (node *)malloc(sizeof(node));
    t->next = v1->point;
    v1->point = t;
    t->point = v2;
    return;
}

// Function to print a graph
void printgraph(node *g) {
    node *t1, *t2, *t3;
    printf("\n Vertex\t Edgelist\n");
    t1 = g;
    while (t1 != 0) {
        printf("\n%d\t", t1->data);
        t2 = t1->point;
        while (t2 != 0) {
            t3 = t2->point;
            printf("%d ", t3->data);
            t2 = t2->next;
        }
        t1 = t1->next;
    }
}

// Enqueue operation
void enque(node *s) {
    int r1 = rear;
    r1 = (r1 + 1) % SIZE;
    if (front == r1) {
        printf("Queue full\n");
        exit(1);
    }
    rear = r1;
    q[rear] = s;
}

// Empty queue to test queue empty or not
int empty() {
    if (front == rear)
        return 1;
    else
        return 0;
}

// Dequeue operation
node *deque() {
    if (empty()) {
        printf("Queue empty\n");
        exit(2);
    }
    front = (front + 1) % SIZE;
    return q[front];
}

// BFS visit with search
void bfs_search(node *s, int search_value) {
    node *t = g, *t1, *u;
    int found = 0;

    while (t != 0) {
        t->status = 0; // Set all vertices as not visited
        t = t->next;
    }
    s->status = 1; // Visit start vertex
    printf("%d ", s->data);

    // Check if the starting vertex matches the search value
    if (s->data == search_value) {
        printf("\nValue %d found at start vertex!\n", search_value);
        return;
    }

    enque(s);
    while (!empty()) {
        u = deque();
        t = u->point;
        while (t != 0) {
            t1 = t->point;
            if (t1->status == 0) {
                printf("%d ", t1->data);
                t1->status = 1;

                // Check if this vertex matches the search value
                if (t1->data == search_value) {
                    printf("\nValue %d found!\n", search_value);
                    found = 1;
                    return;
                }

                enque(t1);
            }
            t = t->next;
        }
    }

    // If the value was not found
    if (!found) {
        printf("\nValue %d not found in the graph.\n", search_value);
    }
}

// Main function
int main() {
    addvertices(1);
    addvertices(2);
    addvertices(3);
    addvertices(4);
    addvertices(5);
    addedge(1, 2);
    addedge(1, 4);
    addedge(2, 3);
    addedge(2, 4);
    addedge(4, 3);
    addedge(4, 5);

    printf("The graph is:\n");
    printgraph(g);

    printf("\n BFS traverse: ");
    bfs_search(find(1), 3);

    printf("\n\nSearching for value 6 in the graph:\n");
    bfs_search(find(1), 6);

    return 0;
}

