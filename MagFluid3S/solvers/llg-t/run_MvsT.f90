program run_MvsT

    ! Perform the MvsT simulation.
    !
    ! Input:
    ! - External Parameters File  
    ! - Internal Parameters File          
    ! - ZFC Initial Microstates File
    ! - FC Initial Microstates File
    
    !
    ! Output:  
    ! - Signals File
    ! - ZFC Cooling Microstates File    
    ! - FC Cooling Microstates File    
    ! - ZFC Evolution Microstates Files    
    ! - FC Evolution Microstates Files 
    !
    ! Used by:
    ! - run.run

    use physics, only: T_, H_, ETA_, Z_, SH_, S0_
    use integration, only: evolution
    integer             :: N, X1, X2
    real*8              :: Ti, Tf, HS, H0, HK, alp, dt
    real*8, allocatable :: Rm, Rp, Om, Op(:), Mu(:), Em_ZFC(:, :), Em_FC(:, :), En_ZFC(:, :), En_FC(:, :), Z(:), SH(:), S0(:)
    real*8              :: t, tt, T0, eta, HS_ZFC(0:2), HS_FC(0:2), H(0:2)
    character(len=100)  :: header, filename    
    integer             :: i, k1, k2
    
!----------------------------------------------------------------------------------------------------------------------------------------------------------

    ! Read and Write Files
    open(100, file='./solvers/llg-t/temporal/Parameters/External.txt', action='read')
    open(101, file='./solvers/llg-t/temporal/Parameters/Intrinsic.txt', action='read')
    open(102, file='./solvers/llg-t/temporal/ZFC Microstates/Initial.txt', action='read')    
    open(103, file='./solvers/llg-t/temporal/FC Microstates/Initial.txt', action='read')        
    open(104, file='./solvers/llg-t/temporal/ZFC Microstates/Cooling.txt', action='write')
    open(105, file='./solvers/llg-t/temporal/FC Microstates/Cooling.txt', action='write')
    open(106, file='./solvers/llg-t/temporal/Signals.txt', action='write')
    write(104, '(A1,A21,A23,A23,A23,A23,A23)') '#', 'Em_x [n.u.]', 'Em_y [n.u.]', 'Em_z [n.u.]', &
                                                    'En_x [n.u.]', 'En_y [n.u.]', 'En_z [n.u.]' 
    write(105, '(A1,A21,A23,A23,A23,A23,A23)') '#', 'Em_x [n.u.]', 'Em_y [n.u.]', 'Em_z [n.u.]', &
                                                    'En_x [n.u.]', 'En_y [n.u.]', 'En_z [n.u.]'                                                   
    write(106, '(A1,A20,A23,A23,A23,A22)') '#', 't [s]', 'H_x [A/m]', 'H_y [A/m]', 'H_z [A/m]', 'T [K]'             
    read(100, '(A)') header
    read(101, '(A)') header
    read(102, '(A)') header 
    read(103, '(A)') header 
    
!----------------------------------------------------------------------------------------------------------------------------------------------------------

    ! Initial Conditions   
    read(100, *) N, Ti, Tf, HS, H0, HK, alp, dt, X1, X2                                                                      ! Read External Parameters
    allocate(Rm, Rp, Om, Op(0:N-1), Mu(0:N-1), Em_ZFC(0:N-1, 0:2), Em_FC(0:N-1, 0:2), En_ZFC(0:N-1 ,0:2), En_FC(0:N-1, 0:2)) ! Allocate Scalars and Arrays
    allocate(Z(0:N-1), SH(0:N-1), S0(0:N-1))                                                                                 ! Allocate Arrays
    read(101, *) (Rm, Rp, Om, Op(i), Mu(i), i=0,N-1)                                                                         ! Read Internal Parameters
    read(102, *) (Em_ZFC(i, :), En_ZFC(i, :), i=0,N-1)                                                                       ! Read ZFC Initial Conditions
    read(103, *) (Em_FC(i, :), En_FC(i, :), i=0,N-1)                                                                         ! Read FC Initial Conditions
    
    tt     = X1 * X2 * dt            ! Total Time   
    HS_ZFC = H_(0.0d0, 0.0d0, 0.0d0) ! Magnetic Field (ZFC Saturation)
    HS_FC  = H_(HS, 0.0d0, 0.0d0)    ! Magnetic Field (FC Saturation)
    H      = H_(H0, 0.d0, 0.0d0)     ! Magnetic Field (Cooling)    
         
!----------------------------------------------------------------------------------------------------------------------------------------------------------
    
    ! Cooling
    t   = 0.0d0                                                                       ! Current Time
    T0  = T_(Ti, Tf, tt, t)                                                           ! Temperature  
    eta = ETA_(T0)                                                                    ! Solvent Viscosiy
    Z   = Z_(N, Op, eta)                                                              ! Drag Coefficients
    SH  = SH_(N, Mu, T0, alp, dt)                                                     ! Thermal Field Standard Deviations
    S0  = S0_(N, Z, T0, dt)                                                           ! Thermal Torque Standard Deviations
    do k2 = 1, 10*X2
        call evolution(N, Mu, Em_ZFC, En_ZFC, Z, SH, S0, HS_ZFC, HS_ZFC, HK, alp, dt) ! ZFC Evolution
        call evolution(N, Mu, Em_FC, En_FC, Z, SH, S0, HS_FC, HS_FC, HK, alp, dt)     ! FC Evolution
    end do

    ! Save Cooling Microstates
    write(104, '(E22.15, E23.15, E23.15, E23.15, E23.15, E23.15)') (Em_ZFC(i, :), En_ZFC(i, :), i=0,N-1)
    write(105, '(E22.15, E23.15, E23.15, E23.15, E23.15, E23.15)') (Em_FC(i, :), En_FC(i, :), i=0,N-1)    
    
    ! Evolution
    do k1 = 1, X1
        do k2 = 1, X2
            T0  = T_(Ti, Tf, tt, t)                                             ! Temperature  
            eta = ETA_(T0)                                                      ! Solvent Viscosiy
            Z   = Z_(N, Op, eta)                                                ! Drag Coefficients
            SH  = SH_(N, Mu, T0, alp, dt)                                       ! Thermal Field Standard Deviations
            S0  = S0_(N, Z, T0, dt)                                             ! Thermal Torque Standard Deviations
            t   = t + dt                                                        ! Next Time            
            call evolution(N, Mu, Em_ZFC, En_ZFC, Z, SH, S0, H, H, HK, alp, dt) ! ZFC Evolution
            call evolution(N, Mu, Em_FC, En_FC, Z, SH, S0, H, H, HK, alp, dt)   ! FC Evolution
        end do

            ! Save Signals
            write(106, '(E21.15, E23.15, E23.15, E23.15, E22.15)') t, H(:), T0

            ! Save ZFC Evolution Microstates
            write(filename, '(A,I3.3,A)') './solvers/llg-t/temporal/ZFC Microstates/', k1, '.txt'
            open(107, file=filename, action='write') 
            write(107, '(A1,A21,A23,A23,A23,A23,A23)') '#', 'Em_x [n.u.]', 'Em_y [n.u.]', 'Em_z [n.u.]', &
                                                            'En_x [n.u.]', 'En_y [n.u.]', 'En_z [n.u.]' 
            write(107, '(E22.15, E23.15, E23.15, E23.15, E23.15, E23.15)') (Em_ZFC(i, :), En_ZFC(i, :), i=0,N-1)
            close(107)

            ! Save FC Evolution Microstates
            write(filename, '(A,I3.3,A)') './solvers/llg-t/temporal/FC Microstates/', k1, '.txt'
            open(108, file=filename, action='write') 
            write(108, '(A1,A21,A23,A23,A23,A23,A23)') '#', 'Em_x [n.u.]', 'Em_y [n.u.]', 'Em_z [n.u.]', &
                                                            'En_x [n.u.]', 'En_y [n.u.]', 'En_z [n.u.]' 
            write(108, '(E22.15, E23.15, E23.15, E23.15, E23.15, E23.15)') (Em_FC(i, :), En_FC(i, :), i=0,N-1)
            close(108)   
    end do    
                          
!----------------------------------------------------------------------------------------------------------------------------------------------------------    

    ! Deallocate Scalars and Arrays, and Close/Delete Files
    deallocate(Rm, Rp, Om, Op, Mu, Em_ZFC, Em_FC, En_ZFC, En_FC, Z, SH, S0)
    close(100); close(101); close(102); close(103); close(104); close(105); close(106)

!----------------------------------------------------------------------------------------------------------------------------------------------------------

end program run_MvsT