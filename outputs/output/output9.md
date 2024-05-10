### Boundary Conditions in Parabolic PDEs

In the study of Parabolic Partial Differential Equations (PDEs), boundary conditions play a crucial role in defining the behavior of the solution within a given domain. Two common types of boundary conditions encountered are Dirichlet boundary conditions and Homogeneous Dirichlet boundary conditions.

#### Dirichlet Boundary Condition

A Dirichlet boundary condition is characterized by setting the function \( u \) equal to a given function \( g \) on the boundary \( OQ \). Mathematically, this condition can be expressed as \( u = g \) on \( OQ \).

#### Homogeneous Dirichlet Boundary Condition

On the other hand, a Homogeneous Dirichlet boundary condition is a special case where the function \( u \) is set to zero on the boundary \( OQ \). This condition is denoted as \( u = 0 \) on \( OQ \).

### Mathematical Representation

For a parabolic PDE of the form \( u_t - Au = f(t, x) \) with \( (t, x) \in ]0, T[ \) and \( x \in \Omega \), where \( \Omega \) represents the spatial domain, the boundary conditions and initial conditions are given as follows:

- Homogeneous Dirichlet boundary condition: \( u|_{\partial \Omega} = 0 \) for \( t \in ]0, T[ \)
- Initial conditions: \( u(0, x) = \phi(x) \) and \( u_t(0, x) = \psi(x) \) for \( x \in \Omega \)

Understanding and appropriately applying these boundary conditions are essential in solving parabolic PDEs with accuracy and efficiency.