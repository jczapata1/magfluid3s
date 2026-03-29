program run_MvsH

    ! Perform the MvsH simulation.
    !
    ! Input:
    ! - External Parameters File  
    ! - Internal Parameters File          
    ! - Initial Microstates File
    !
    ! Output:  
    ! - Signals File
    ! - Saturation Microstates File    
    ! - Evolution Microstates Files
    !
    ! Used by:
    ! - base.run.run

    use physics, only: H_, SH_
    use integration, only: evolution
    integer             :: N, X0, X1, X2
    real*8              :: T0, H0, HK, alp, dt, f
    real*8, allocatable :: Rm, Rp, Om, Op, Mu(:), Em(:, :), En(:, :), SH(:)
    real*8              :: t, Ha(0:2), Hb(0:2)
    character(len=100)  :: header, filename   
    integer             :: i, k0, k1, k2
       
!----------------------------------------------------------------------------------------------------------------

    ! Read and Write Files
    open(100, file='./solvers/llg/temporal/Parameters/External.txt', action='read')
    open(101, file='./solvers/llg/temporal/Parameters/Intrinsic.txt', action='read')
    open(102, file='./solvers/llg/temporal/Microstates/Initial.txt', action='read')    
    open(103, file='./solvers/llg/temporal/Microstates/Saturation.txt', action='write')   
    open(104, file='./solvers/llg/temporal/Signals.txt', action='write') 
    write(103, '(A1,A21,A23,A23,A23,A23,A23)') '#', 'Em_x [n.u.]', 'Em_y [n.u.]', 'Em_z [n.u.]', &
                                                    'En_x [n.u.]', 'En_y [n.u.]', 'En_z [n.u.]' 
    write(104, '(A1,A20,A23,A23,A23,A22)') '#', 't [s]', 'H_x [A/m]', 'H_y [A/m]', 'H_z [A/m]', 'T [K]'  
    read(100, '(A)') header
    read(101, '(A)') header
    read(102, '(A)') header
    
!----------------------------------------------------------------------------------------------------------------  

    ! Initial Conditions
    read(100, *) N, T0, H0, HK, alp, dt, X0, X1, X2, f                             ! Read External Parameters
    allocate(Rm, Rp, Om, Op, Mu(0:N-1), Em(0:N-1, 0:2), En(0:N-1, 0:2), SH(0:N-1)) ! Allocate Scalars and Arrays
    read(101, *) (Rm, Rp, Om, Op, Mu(i), i=0,N-1)                                  ! Read Internal Parameters
    read(102, *) (Em(i, :), En(i, :), i=0,N-1)                                     ! Read Initial Conditions
    
    SH = SH_(N, Mu, T0, alp, dt) ! Thermal Field Standard Deviations
    
!---------------------------------------------------------------------------------------------------------------- 
    
    ! Saturation
    t = 0.0d0                                              ! Initial Time
    Ha = H_(H0, f, t)                                      ! Magnetic Field
    do k2 = 1, 10*X2
        call evolution(N, Em, En, SH, Ha, Ha, HK, alp, dt) ! Evolution
    end do

    ! Save Saturation Microstates
    write(103, '(E22.15, E23.15, E23.15, E23.15, E23.15, E23.15)') (Em(i, :), En(i, :), i=0,N-1)

    ! Evolution
    do k0 = 1, X0
        do k1 = 1, X1
            do k2 = 1, X2
                Ha = H_(H0, f, t)                                  ! Magnetic Field -> H = H(t)                
                Hb = H_(H0, f, t + dt)                             ! Magnetic Field -> H = H(t+dt)
                t  = t + dt                                        ! Next Time
                call evolution(N, Em, En, SH, Ha, Hb, HK, alp, dt) ! Evolution
            end do

            ! Save Signals
            write(104, '(E21.15, E23.15, E23.15, E23.15, E22.15)') t, Hb(:), T0

            ! Save Evolution Microstates
            write(filename, '(A,I2.2,A,I3.3,A)') './solvers/llg/temporal/Microstates/', k0, '_', k1, '.txt'
            open(105, file=filename, action='write') 
            write(105, '(A1,A21,A23,A23,A23,A23,A23)') '#', 'Em_x [n.u.]', 'Em_y [n.u.]', 'Em_z [n.u.]', &
                                                            'En_x [n.u.]', 'En_y [n.u.]', 'En_z [n.u.]' 
            write(105, '(E22.15, E23.15, E23.15, E23.15, E23.15, E23.15)') (Em(i, :), En(i, :), i=0,N-1)
            close(105)
        end do
    end do

!----------------------------------------------------------------------------------------------------------------      

    ! Deallocate Scalars and Arrays, and Close/Delete Files
    deallocate(Rm, Rp, Om, Op, Mu, Em, En, SH)
    close(100); close(101); close(102); close(103); close(104)

!----------------------------------------------------------------------------------------------------------------

end program run_MvsH