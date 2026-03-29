program run_Microstates

    ! Perform the Microstates simulation.
    !
    ! Input:
    ! - External Parameters File  
    ! - Internal Parameters File          
    ! - Initial Microstates File
    !
    ! Output:  
    ! - Signals File  
    ! - Evolution Microstates Files
    !
    ! Used by:
    ! - base.run.run

    use physics, only: H_, SH_
    use integration, only: evolution
    integer             :: N, X2
    real*8              :: T0, H0, HK, alp, dt
    real*8, allocatable :: Rm, Rp, Om, Op, Mu(:), Em(:, :), En(:, :), SH(:)
    real*8              :: t, H(0:2)
    character(len=100)  :: header, filename   
    integer             :: i, k2
    
!----------------------------------------------------------------------------------------------------------------  

    ! Read and Write Files
    open(100, file='./solvers/llg/temporal/Parameters/External.txt', action='read')
    open(101, file='./solvers/llg/temporal/Parameters/Intrinsic.txt', action='read')
    open(102, file='./solvers/llg/temporal/Microstates/Initial.txt', action='read')    
    open(103, file='./solvers/llg/temporal/Signals.txt', action='write') 
    write(103, '(A1,A20,A23,A23,A23,A22)') '#', 't [s]', 'H_x [A/m]', 'H_y [A/m]', 'H_z [A/m]', 'T [K]'  
    read(100, '(A)') header
    read(101, '(A)') header 
    read(102, '(A)') header 

!---------------------------------------------------------------------------------------------------------------- 

    ! Initial Conditions
    read(100, *) N, T0, H0, HK, alp, dt, X2                                        ! Read External Parameters
    allocate(Rm, Rp, Om, Op, Mu(0:N-1), Em(0:N-1, 0:2), En(0:N-1, 0:2), SH(0:N-1)) ! Allocate Scalars and Arrays
    read(101, *) (Rm, Rp, Om, Op, Mu(i), i=0,N-1)                                  ! Read Internal Parameters
    read(102, *) (Em(i, :), En(i, :), i=0,N-1)                                     ! Read Initial Conditions
    
    SH = SH_(N, Mu, T0, alp, dt) ! Thermal Field Standard Deviations
    H  = H_(H0, 0.0d0, 0.0d0)    ! Magnetic Field
       
!----------------------------------------------------------------------------------------------------------------     
      
    ! Evolution
    t = 0.0d0 ! Initial Time    
    do k2 = 1, X2    
        t = t + dt                                       ! Next Time
        call evolution(N, Em, En, SH, H, H, HK, alp, dt) ! Evolution
    
        ! Save Signals
        write(103, '(E21.15, E23.15, E23.15, E23.15, E22.15)') t, H(:), T0

        ! Save Evolution Microstates
        write(filename, '(A,I4.4,A)') './solvers/llg/temporal/Microstates/', k2, '.txt'
        open(104, file=filename, action='write') 
        write(104, '(A1,A21,A23,A23,A23,A23,A23)') '#', 'Em_x [n.u.]', 'Em_y [n.u.]', 'Em_z [n.u.]', &
                                                        'En_x [n.u.]', 'En_y [n.u.]', 'En_z [n.u.]' 
        write(104, '(E22.15, E23.15, E23.15, E23.15, E23.15, E23.15)') (Em(i, :), En(i, :), i=0,N-1)
        close(104)
    end do
    
!----------------------------------------------------------------------------------------------------------------

    ! Deallocate Scalars and Arrays, and Close/Delete Files
    deallocate(Rm, Rp, Om, Op, Mu, Em, En, SH)
    close(100); close(101); close(102); close(103)
    
!----------------------------------------------------------------------------------------------------------------  

end program run_Microstates