using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

[RequireComponent(typeof(NavMeshAgent))]
public class ReaperBase : MonoBehaviour
{
    [SerializeField] protected float totalHealth, currentHealth;
    
    protected NavMeshAgent navAgent;
    [SerializeField] protected bool isDead;
    protected Coroutine lifeRoutine;

    [SerializeField] protected GameObject playerCharacter;
    // Start is called before the first frame update
    protected void Awake()
    {
        navAgent = GetComponent<NavMeshAgent>();
        currentHealth = totalHealth;
    }

    protected void MakeDead()
    {
        isDead = true;
    }
    
}
